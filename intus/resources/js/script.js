let = document.getElementById('loader');

let posts = [];

let lastModifiedDate = '';

let currentAmountOfPosts = 0;

let currentMediaIndex = 0;

let mediaElements = [];

let amountOfMedia = mediaElements.length;

let deletedPosts = [];

let addedPosts = [];

window.addEventListener('load', (event) => {


    // Code starts here
    setTimeout(() => {
        getFirstData();
    }, 0)

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
                    throw new Error ('no  showcase.json or error with local server');
                }

                return response.json();
            })
            .then(data => {
                // Means there's not a single post for the display
                if(data.length == 0) {
                    throw new Error ('no posts for the current display');
                }

                let responsePosts = data;

                appendAddedPosts(responsePosts);

                if(addedPosts.length > 0) {
                    addPosts(addedPosts);                    
                }

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
        if(posts.length == 0) {

            showNoContent();

        } else {
            let post = posts[currentMediaIndex];

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

                        // Checks if there are any new posts to create
                        if(addedPosts.length > 0) {
                            addPosts(addedPosts);
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

                if (response.status == 302) {
                    throw new Error ('not modified');
                }

                return response.json();
            })
            .then(data => {
                console.log('data inside fetchupdate: ', data);
                let posts_lenght_before_fetch = posts.length;

                let responsePosts = data;

                if(responsePosts.length > currentAmountOfPosts) {

                    appendAddedPosts(responsePosts);
                    

                } else if(responsePosts.length < currentAmountOfPosts) {

                    appendDeletedPosts(responsePosts);

                }

                if(posts_lenght_before_fetch == 0) {
                    addPosts(addedPosts);

                    nextPost();
                }
            })
            .catch(error => {

                console.error(error);

                if(posts.length == 0) {
                    showNoContent();
                }

            })
    }

    function showNoContent()
    {
        console.log('showNOContent');

        // Apply class selected only if not already selected
        if(!loader.classList.contains('selected')) {
            loader
                .classList.add('selected');
        }

        setTimeout(() => {
            checkPostsUpdate();
        }, 5000);
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

    function appendAddedPosts(responsePosts)
    {
        let newPosts = getNewPosts(responsePosts);

        newPosts.forEach(newPost => {
            addedPosts.push(newPost)
        });        
    }      

    function createAddedPost(newPost)
    {        
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
    }

    function addEventToVideo(video)
    {
        video.addEventListener('ended', function(e) {
            mediaElements[currentMediaIndex]
                .classList.remove("selected");

            if(deletedPosts.includes(mediaElements[currentMediaIndex])) {
                removePost(currentMediaIndex);
            }

            // Checks if there are any new posts to create
            if(addedPosts.length > 0) {
                addPosts(addedPosts);
            }

            currentMediaIndex++;

            if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
            }

            nextPost();
        });
    }

    function addPosts(addedPosts)
    {
        addedPosts.forEach((addedPost) => {
            createAddedPost(addedPost)
            posts.push(addedPost);
        });
        
        mediaElements = document.querySelectorAll("#slider img, video");
        amountOfMedia = mediaElements.length;
        currentAmountOfPosts = posts.length;

        addedPosts.splice(0, addedPosts.length)
    }

    function removePost(currentMediaIndex)
    {
        mediaElements[currentMediaIndex].remove();
        deletedPosts = spliceDeletedPosts(mediaElements[currentMediaIndex], deletedPosts);
        posts.splice(currentMediaIndex, 1);

        currentAmountOfPosts = posts.length;
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

    function getNewPosts(responsePosts)
    {
        let result = responsePosts.filter(function (o1) {
            return !posts.some(function (o2) {
                return o1.post_id === o2.post_id; // return the ones with equal id
           });
        });

        return result;
    }  
});

