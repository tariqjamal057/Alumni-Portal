const text = document.querySelector('.event-desc');

var path = window.location.pathname;

if(path == '/') {
    const result = text.slice(0,100);
    text.innerHTML = result;
}


