$('.share-btn').click(function(){
    $(this).addClass("clicked");
});

$('.close').click(function (e) {
  $('.clicked').removeClass('clicked');
  e.stopPropagation();
});
