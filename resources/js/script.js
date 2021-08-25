window.addEventListener('load', (event) => {

    let currentAmountOfPosts = posts.length;
    let currentMediaIndex = 0;
    let mediaElements = document.querySelectorAll("#slider img, video");
    let amountOfMedia = mediaElements.length;

    let deletedPosts = [];

    function nextPost()    
    {
        console.log('deletedPosts: ', deletedPosts);
        if(mediaElements[currentMediaIndex].tagName == 'IMG') {
            mediaElements[currentMediaIndex]
                .classList.add("selected");
            console.log('selected post: ', mediaElements[currentMediaIndex]);

            let post = posts[currentMediaIndex];

            let duration = post.media_duration;

            setTimeout(() => {
                mediaElements[currentMediaIndex]
                    .classList.remove("selected"); 
                console.log('inside setTimout after removing class selected');
                
                removeDeletedPost(mediaElements[currentMediaIndex]);

                currentMediaIndex++;

                if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
                }

                nextPost();
            }, duration);

        } else if(mediaElements[currentMediaIndex].tagName == 'VIDEO') {
            console.log(mediaElements[currentMediaIndex]);

            mediaElements[currentMediaIndex]
                .classList.add("selected");

            var vid = mediaElements[currentMediaIndex];

            vid.play();
        }

        checkPostsUpdate();           
    }

    let lastModifiedDate = '';

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
                } else if(responsePosts.length < currentAmountOfPosts) {                    
                    appendDeletedPosts(responsePosts);
                }

                posts = responsePosts;
                currentAmountOfPosts = responsePosts.length;                
            })
            .catch(error => {
                console.error(error);
            })
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

    function removeDeletedPost(mediaElement)
    {
        if(deletedPosts.includes(mediaElement)) {
            console.log('deletedPosts', deletedPosts);
            console.log('include: ', deletedPosts.includes(mediaElement));
            mediaElement.remove();
            const index = deletedPosts.indexOf(mediaElement)
            if (index > -1) {
                deletedPosts.splice(index, 1);
                mediaElements = document.querySelectorAll("#slider img, video");
                amountOfMedia = mediaElements.length;
            }
            console.log(deletedPosts);
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
            
            removeDeletedPost(mediaElements[currentMediaIndex]);

            currentMediaIndex++;

            if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
            }

            nextPost();
        });
    }

    const videos = document.querySelectorAll('video');
    if(videos.length > 0) {
        videos.forEach(function(video) {
            addEventToVideo(video);
        });

        nextPost();
    } else {
        nextPost();
    }

});