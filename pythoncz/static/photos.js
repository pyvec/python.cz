
var displayDuration = 5000; // ms
var fadeDuration = 2000; // ms


function show($images, index) {
    var current = index % $images.length;
    var $current = $($images[current]);

    var next = (index + 1) % $images.length;
    var $next = $($images[next]);

    $current.show();
    $images.not($current).hide();

    $next.delay(displayDuration).fadeIn(fadeDuration);
    $current.delay(displayDuration).fadeOut(fadeDuration, function() {
        show($images, next);
    });
}


$(function() {
    var $images = $('.photo-container .photo');
    show($images, $images.length - 1); // beginning with the last one (visible)
});
