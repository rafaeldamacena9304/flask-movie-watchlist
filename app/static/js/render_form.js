document.addEventListener('DOMContentLoaded', function() {
    movieModal = document.getElementById('movieModal');
    openMovieModal = document.getElementById('openMovieModal');
    closeMovieModal = document.getElementById('closeMovieModal');

    openMovieModal.addEventListener('click', function(){
        movieModal.style.display = 'block'
    })
    closeMovieModal.addEventListener('click', function(){
        movieModal.style.display = 'none'
    })
});