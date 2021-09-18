let = document.getElementById('loader');

let posts = [];

let lastModifiedDate = '';

let currentAmountOfPosts = 0;

let currentMediaIndex = 0;

let mediaElements = [];

let loop = 0;

let amountOfMedia = mediaElements.length;
    
let deletedPosts = [];

window.addEventListener('load', (event) => {    
    

    // Code starts here 
    setTimeout(() => {
        getFirstData(); 
    }, 10000)
    

    function getFirstData()
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
                console.log('response status getFirstData: ', response.status);
                lastModifiedDate = response.headers.get('Last-Modified');                

                if (response.status != 200) {                    
                    throw new Error ('no local_data.json or error with local server');
                }     

                return response.json();
            })
            .then(data => {
                // Means there's not a single post for the display
                if(data.length == 0) {
                    throw new Error ('no posts for the current display');
                }

                let responsePosts = data;                                

                createAddedPosts(responsePosts);

                mediaElements = document.querySelectorAll("#slider img, video");

                amountOfMedia = mediaElements.length;

                posts = responsePosts;

                currentAmountOfPosts = responsePosts.length;  
                
                nextPost();
            })
            .catch(error => {

                console.error(error);

                showNoContent();

            })
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

            currentMediaIndex++;

        
            if(currentMediaIndex >= amountOfMedia) {
                
                currentMediaIndex = 0;
                
                
                loop++;

                // If enter here, means already passed through 
                // the whole posts array 2 times, meaning there isn't any
                // current posts to display.
                // This is need so the code doesn't enter an infinte loop
                if(loop > 1) {

                    loop = 0;

                    showNoContent();

                } else {
                    // Continue to check one more complete loop
                    nextPost();
                }

            } else {
                // Means there're other posts to check
                nextPost();
            }            
        } else {
            // Need to reset the loop, otherwise it will keep couting
            // even if there are 1 post to show but any other not
            loop = 0;

            // If the loader is selected, removes it to show the post
            if(loader.classList.contains('selected')) {
                console.log('selected');
                loader
                    .classList.remove('selected');
            }

            // Checkes whether the element is an image or video
            switch(mediaElements[currentMediaIndex].tagName) {
                case 'IMG':
                    let duration = post.media_duration;

                    mediaElements[currentMediaIndex]
                        .classList.add("selected");
 
                    // Waits for the duration of the media image to enter
                    // the function
                    setTimeout(() => {
                        mediaElements[currentMediaIndex]
                            .classList.remove("selected");                 
                        
                        // After showing the image, checks if it has been removed
                        // and deletes it if yes.
                        if(deletedPosts.includes(mediaElements[currentMediaIndex])) {
                            removePost(currentMediaIndex);
                        }
        
                        currentMediaIndex++;
        
                        if(currentMediaIndex >= amountOfMedia) {
                            currentMediaIndex = 0;
                        }

                        checkPostsUpdate(false);

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
        }  
    }

    function checkPostsUpdate(no_content)
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
            .finally(() => {
                console.log('reach finally');

                if(no_content) { 
                    showNoContent();
                } else {
                    nextPost();
                }
            });
    }

    function showNoContent()
    {
        console.log('showNOContent');        

        // Apply class selected only if not already selected
        if(!loader.classList.contains('selected')) {
            loader
                .classList.add('selected');
        }

        // Keeps checking if should show any current posts.
        // If not, fetches the server for updated in the JSON posts.
        // Does it every 5 seconds.
        setTimeout(() => {
            console.log('prox chamado é shouldShowAnyCurrentPost');
            if(shouldShowAnyCurrentPosts()) {
                nextPost();
            } else {
                checkPostsUpdate(true);
            }

        }, 5000);

    }

    function shouldShowAnyCurrentPosts()
    { 
        let control = false;
        posts.forEach((post) => {
            console.log('post inside shouldShowAnyCurrentPosts: ', post);

            const date_now        = new Date();   
            const post_start_date = new Date(post.start_date);
            const post_end_date   = new Date(post.end_date);        

            const date_and_times = getDateAndTimes(post_start_date, post_end_date, date_now);              

            console.log(date_and_times);

            console.log('shouldShow: ', shouldShow(date_and_times));

            if(shouldShow(date_and_times)) {
                console.log('shouldShowAnyCurrentPosts = true');
                control = true;
            }
        });
        console.log('shouldShowAnyCurrentPosts control: ', control);
        return control;
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
                removePost(currentMediaIndex);
            }

            currentMediaIndex++;

            if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
            }

            checkPostsUpdate(false);
        });
    }

    function removePost(currentMediaIndex)
    {
        mediaElements[currentMediaIndex].remove();
        deletedPosts = spliceDeletedPosts(mediaElements[currentMediaIndex], deletedPosts);

        posts.splice(currentMediaIndex, 1);
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
                hour: post_end_date.getHours(),
                minute: post_end_date.getMinutes(),
            },
        };


        return object_with_dates;
    }

    function shouldShow(date_and_times)
    {
        console.log('inside shouldShow');
        // Verificação 1: se a data de ínicio do posta for <= ao dia de hoje, significa que
        // já pode ser mostrado, pela data. Caso contrário, ainda não deve
        // ser mostrado.
        if(date_and_times.start.date_sum <= date_and_times.now.date_sum) {
            // Verificação 2: data de fim precisa ser >= ao dia de hoje, do
            // contrário, já passou da data de fim e não deve ser mostrado.           
            if(date_and_times.end.date_sum >= date_and_times.now.date_sum) {  
                // Verificações 3: já sei que posso mostrar, pelos dias, mas
                // preciso verificar as horas.
                
                if(date_and_times.start.hour <= date_and_times.now.hour
                    && date_and_times.end.hour > date_and_times.now.hour) {
                        // Se a hora de ínicio já passou ainda não estou na 
                        // hora de fim, posso mostrar, pois não
                        // preciso verificar os minutos.    
                        return true;
                }

                // Se a hora de ínicio é a mesma da atual, preciso verificar
                // os minutos de início e fim
                if(date_and_times.start.hour == date_and_times.now.hour) {

                    if(date_and_times.start.minute <= date_and_times.now.minute
                        && date_and_times.end.minute > date_and_times.now.minute) {                        
                        return true;                        
                    }

                }

                // Sei que posso mostrar pela hora, pois já passou da hora
                // de ínicio da postagem, não preciso verificar mais as horas
                // e minutos de ínicio, somente de fim
                if(date_and_times.start.hour < date_and_times.now.hour) {
                    
                    if(date_and_times.end.hour > date_and_times.now.hour
                        && date_and_times.end.minute > date_and_times.now.minute) {
                        // Não preciso verificar os minutos, pois sei que
                        // não vai terminar nessa hora ainda.
                        return true;
                    }

                }
            } 
        } 

        return false;
    }

    function getSumDate(date_object)
    {
        return date_object.getFullYear() + date_object.getMonth() + date_object.getDay();
    }
});

