window.addEventListener('load', (event) => {

    let currentAmountOfPosts = posts.length;
    let currentMediaIndex = 0;
    let mediaElements = document.querySelectorAll("#slider img, video");
    let amountOfMedia = mediaElements.length;
    let loop = 0;

    let deletedPosts = [];
    let lastModifiedDate = '';

    // Code starts running here
    const videos = document.querySelectorAll('video');

    if(videos.length > 0) {
        videos.forEach(function(video) {
            addEventToVideo(video);
        });

        nextPost();
    } else {
        nextPost();
    }

    // Function Declarations
    function nextPost()    
    {
        let post = posts[currentMediaIndex];

        let date_now        = new Date();   
        let post_start_date = new Date(post.start_date);
        let post_end_date   = new Date(post.end_date);        

        let date_and_times = getDateAndTimes(post_start_date, post_end_date, date_now);              

        if(!shouldShow(date_and_times)) {
            console.log('oi dentro');
            currentMediaIndex++;
            console.log('currentMediaIndex: ', currentMediaIndex);
            if(currentMediaIndex >= amountOfMedia) {
                console.log('currentMediaIndex dentro do if: ', currentMediaIndex);
                currentMediaIndex = 0;
                console.log('currentMediaIndex depois de zerar: ', currentMediaIndex);
                loop++;
                console.log('loop: ', loop);
                if(loop > 1) {
                    console.log('inside if');
                    showNoContent();
                } else {
                    nextPost();
                }                
            } else {
                nextPost();
            }            
        } else {
            switch(mediaElements[currentMediaIndex].tagName) {
                case 'IMG':
                    let duration = post.media_duration;

                    mediaElements[currentMediaIndex]
                        .classList.add("selected");

                    console.log('selected post: ', mediaElements[currentMediaIndex]);
 
                    setTimeout(() => {
                        mediaElements[currentMediaIndex]
                            .classList.remove("selected");                 
                        
                        if(deletedPosts.includes(mediaElements[currentMediaIndex])) {
                            mediaElements[currentMediaIndex].remove();
                            deletedPosts = spliceDeletedPosts(mediaElements[currentMediaIndex], deletedPosts);
        
                            posts.splice(currentMediaIndex, 1);
                        }
        
                        currentMediaIndex++;
        
                        if(currentMediaIndex >= amountOfMedia) {
                            currentMediaIndex = 0;
                        }
        
                        nextPost();
                    }, duration);

                    break;

                case 'VIDEO':
                    console.log(mediaElements[currentMediaIndex]);
    
                    mediaElements[currentMediaIndex]
                        .classList.add("selected");
        
                    var vid = mediaElements[currentMediaIndex];
        
                    vid.play();

                    break;
            } 
            checkPostsUpdate();               
        }  
    }

    function checkPostsUpdate()
    {
        let myHeaders = new Headers();

        myHeaders.append('If-Modified-Since', lastModifiedDate);
        myHeaders.append('Content-Type', 'application/json');

        let myRequest = new Request('http://localhost:8000', {
            method: 'GET',
            headers: myHeaders,
            mode: 'cors',
        });

        fetch(myRequest)
            .then(response => {
                console.log('response status: ', response.status);
                lastModifiedDate = response.headers.get('Last-Modified');
                console.log('lastModifiedDate: ', lastModifiedDate);
                if (response.status == 302) {                    
                    throw new Error ('not modified');
                }                
                return response.json();
            })
            .then(data => {
                let responsePosts = data;
                
                if(responsePosts.length > currentAmountOfPosts) {
                    createAddedPosts(responsePosts);
                    mediaElements = document.querySelectorAll("#slider img, video");
                    amountOfMedia = mediaElements.length;

                    posts = responsePosts;
                } else if(responsePosts.length < currentAmountOfPosts) {                    
                    appendDeletedPosts(responsePosts);
                }

                currentAmountOfPosts = responsePosts.length;                
            })
            .catch(error => {
                console.error(error);
            })
    }

    function showNoContent()
    {
        console.log('showNOContent');
        const loader = document.getElementById('loader');

        loader.classList.add('selected');


    }

    function appendDeletedPosts(responsePosts)
    {
        const responsePostsIds = [];
        const currentPostsIds = [];

        responsePosts.forEach(function(e) {
            responsePostsIds.push(e.post_id);
        });
        posts.forEach(function(e) {
            currentPostsIds.push(e.post_id);
        });

        let removedPostsIds = currentPostsIds.filter(x => !responsePostsIds.includes(x));        
        console.table(removedPostsIds);

        removedPostsIds.forEach(removedPostId => {
            const deleteElement = document.getElementById(removedPostId);
            deletedPosts.push(deleteElement);
        })

    }

    function spliceDeletedPosts(mediaElement, oldDeletedPosts)
    {    
        const index = deletedPosts.indexOf(mediaElement);

        if (index > -1) {
            oldDeletedPosts.splice(index, 1);
            mediaElements = document.querySelectorAll("#slider img, video");
            amountOfMedia = mediaElements.length;
            
            return oldDeletedPosts;
        }
    }

    

    function createAddedPosts(responsePosts)
    {
        let newPosts = responsePosts.slice(currentAmountOfPosts);

        newPosts.forEach(function(newPost) {
            switch(newPost.media_type) {
                case 'image':
                    let newImage = document.createElement('img');

                    newImage.id  = newPost.post_id;
                    newImage.src = newPost.local_path;
                    newImage.alt = newPost.media_name;

                    slider.appendChild(newImage);
                    break;

                case 'video':
                    let newVideo    = document.createElement('video');
                    let newSource   = document.createElement('source');

                    newVideo.id     = newPost.post_id;
                    newVideo.width  = 1920;
                    newVideo.height = 1080;
                    newVideo.muted  = true;
                    newSource.type  = newPost.media_type + '/' + newPost.media_extension;
                    newSource.src   = newPost.local_path;

                    newVideo.appendChild(newSource);
                    slider.appendChild(newVideo);

                    addEventToVideo(newVideo);
                    break;
            }
        });
    }

    

    function addEventToVideo(video)
    {
        video.addEventListener('ended', function(e) {
            mediaElements[currentMediaIndex]
                .classList.remove("selected");
            
            if(deletedPosts.includes(mediaElements[currentMediaIndex])) {
                mediaElements[currentMediaIndex].remove();
                deletedPosts = spliceDeletedPosts(mediaElements[currentMediaIndex], deletedPosts);

                posts.splice(currentMediaIndex, 1);
            }

            currentMediaIndex++;

            if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
            }

            nextPost();
        });
    }

    // Functions Declarations
    function getDateAndTimes(post_start_date, post_end_date, date_now)
    {

        let object_with_dates;
        
        object_with_dates = {
            now: {
                date_sum: getSumDate(date_now),
                hour: date_now.getHours(),
                minute: date_now.getMinutes(),
            },
            start: {
                date_sum: getSumDate(post_start_date),
                hour: post_start_date.getHours(),
                minute: post_start_date.getMinutes(),
            },
            end: {
                date_sum: getSumDate(post_end_date),
                hour: post_start_date.getHours(),
                minute: post_end_date.getMinutes(),
            },
        };


        return object_with_dates;
    }

    function shouldShow(date_and_times)
    {
        if(betweenStartEnd(date_and_times.now.date_sum, date_and_times.start.date_sum, date_and_times.end.date_sum)) {
            if(betweenStartEnd(date_and_times.now.hour, date_and_times.start.hour, date_and_times.end.hour)) {     
                if(betweenStartEnd(date_and_times.now.minute, date_and_times.start.minute, date_and_times.end.minute)) {
                    return true;                
                }    
            }
        }

        return false;
    }

    function getSumDate(date_object)
    {
        return date_object.getFullYear() + date_object.getMonth() + date_object.getDay();
    }

    function betweenStartEnd(now_value, start_value, end_value)
    {
        return start_value <= now_value && end_value >= now_value;
    }

});

