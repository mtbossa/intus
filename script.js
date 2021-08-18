window.addEventListener('load', (event) => {

    const posts = [{'post_id': 92, 'media_name': 'teste de imagem', 'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/medias/1/teste-de-imagem.png', 'media_duration': 5000, 'media_type': 'image', 'media_extension': 'png', 'local_path': 'medias/teste-de-imagem.png'}, {'post_id': 95, 'media_name': 'video4', 'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/medias/1/video4.mp4', 'media_duration': 10830, 'media_type': 'video', 'media_extension': 'mp4', 'local_path': 'medias/video4.mp4'}, {'post_id': 103, 'media_name': 'teste de imagem', 'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/medias/1/teste-de-imagem.png', 'media_duration': 5000, 'media_type': 'image', 'media_extension': 'png', 'local_path': 'medias/teste-de-imagem.png'}, {'post_id': 104, 'media_name': 'midia nova', 'media_url': 'https://intus-medias-paineis.s3.amazonaws.com/medias/1/midia-nova.mp4', 'media_duration': 9770, 'media_type': 'video', 'media_extension': 'mp4', 'local_path': 'medias/midia-nova.mp4'}]
    console.log(posts)
    const currentAmountOfPosts = posts.length;

    let firstTime = true;
    let currentMediaIndex = 0;
    let mediaElements = document.querySelectorAll("#slider img, video");
    let amountOfMedia = mediaElements.length;

    function nextPost()
    {
        if(mediaElements[currentMediaIndex].tagName == 'IMG') {
            console.log('inside media');
            mediaElements[currentMediaIndex]
                .classList.add("selected");   
            console.log('inside next post');
            let post = posts[currentMediaIndex];
                
            let duration = post.media_duration;
            console.log(duration);
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