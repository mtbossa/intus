window.addEventListener('load', (event) => {

    let currentAmountOfPosts = posts.length;
    let firstTime = true;
    let currentMediaIndex = 0;
    let mediaElements = document.querySelectorAll("#slider img, video");
    let amountOfMedia = mediaElements.length;

    function nextPost()
    {
        if(mediaElements[currentMediaIndex].tagName == 'IMG') {
            mediaElements[currentMediaIndex]
                .classList.add("selected");

            let post = posts[currentMediaIndex];

            let duration = post.media_duration;

            setTimeout(function() {
                mediaElements[currentMediaIndex]
                    .classList.remove("selected");

                currentMediaIndex++;

                if(currentMediaIndex >= amountOfMedia) {
                currentMediaIndex = 0;
                }

                nextPost();
            }, duration);

        } else if(mediaElements[currentMediaIndex].tagName == 'VIDEO') {

            mediaElements[currentMediaIndex]
                .classList.add("selected");

            var vid = mediaElements[currentMediaIndex];

            vid.play();
        }
    }

    let checkPostsInterval = 5000;
    let lastModifiedDate = '';

    setTimeout(checkPostsUpdate, checkPostsInterval);

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
                if (response.status == 302) {
                    throw new Error ('not modified');
                }
                lastModifiedDate = response.headers.get('Last-Modified');
                return response.json();
            })
            .then(data => {
                const slider = document.getElementById('slider');

                let responsePosts = data;

                if(responsePosts.length > currentAmountOfPosts) {
                    createAddedPosts(responsePosts);
                } else if(responsePosts.length < currentAmountOfPosts) {
                    removeDeletedPosts(responsePosts);
                }

                posts = responsePosts;
                currentAmountOfPosts = responsePosts.length;
                mediaElements = document.querySelectorAll("#slider img, video");
                amountOfMedia = mediaElements.length;

                setTimeout(checkPostsUpdate, checkPostsInterval);
            })
            .catch(error => {
                setTimeout(checkPostsUpdate, checkPostsInterval);
            })
    }

    function removeDeletedPosts(responsePosts)
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
        removedPostsIds.forEach(function(removedPostId) {
            const deleteElement = document.getElementById(removedPostId);
            deleteElement.remove();
        })

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