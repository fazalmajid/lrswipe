$(function() {
  var pictures = [],
    $thumbnails = $('#thumbnails'),
    $title = $('#title'),
    $pause = $('#pause');
  var idx = 0;
  var to_load = $thumbnails.find('li').size();
  //  var jScrollPaneApi;

  // jScrollPane
  $thumbnails.find('ul img').load(function() {
    to_load = to_load - 1;
    var ul = $thumbnails.find('ul');
    //ul.width(ul.width() + 10 + $(this).parent().outerWidth(true));
    $thumbnails.find('ul').width(function() {
      var totalWidth = 0;
      $(this).find('li').each(function() {
        totalWidth += $(this).outerWidth(true);
      });
      return totalWidth;
    });
    if (to_load == 0) {
      $thumbnails.jScrollPane();
      jScrollPaneApi = $thumbnails.data('jsp');
      $(window).bind('resize', function() {
        jScrollPaneApi.reinitialise();
      });
    }
  });

  // Photoswipe
//   var myPhtooSwipe = $thumbnails.find("a").photoSwipe({
//     enableMouseWheel: false , enableKeyboard: false,
//         autoStartSlideshow: true, slideshowDelay: 5000
//   });

  // Vegas Background
  $thumbnails.find('a').each(function() {
    pictures.push({
      src: $(this).attr('href'),
      fname: $(this).attr('id'),
      title: $(this).find('img').attr('alt'),
      desc: $(this).find('img').attr('title'),
      valign: $(this).find('img').data('valign')
    });
  })

  $.vegas('slideshow', {
    backgrounds: pictures,
    delay: 10000,
    walk: function(step) {
      var li = $thumbnails.find("li").eq(step);
      jScrollPaneApi.scrollToElement(li);
      li.first().first().fadeToggle(500);
      li.first().first().fadeToggle(500);
      idx = step;
    }
  })('destroy', 'overlay');
  
  $('body').bind('vegasload', function(e, img) {
    var src = $(img).attr('src'),
      idx = $('a[href="' + src + '"]').parent('li').index();

    $title.fadeOut(function() {
      $(this).find('h1').text(pictures[idx].title);
      $(this).find('#description').text(pictures[idx].desc);
      $(this).find('#info').text(meta[pictures[idx].src.substr(4)]);
      $(this).fadeIn();
    });

  });

  // make normal links work normally
  $('a').click(function() {
    event.stopPropagation();
    return true;
  });

  // Photograph
  $thumbnails.find('a').click(function() {
    //$pause.show();
  
    //$thumbnails.animate({top: '-115px'});
    //$title.animate({bottom: '-115px'});  

    idx = $(this).parent('li').index();
    //$.vegas('slideshow', {step: idx})('pause');
    $.vegas('jump', idx);

    event.stopPropagation();

    return false;
  });

//   $(document.body).click(function() {
//     $pause.show();
//     $.vegas('pause');
//     return false;
//   });

  function goPhotoSwipe() {
    $(document.body).off("click");
    var myPhotoSwipe = $("#thumbnails a").photoSwipe({});
    $.vegas('pause');
    myPhotoSwipe.addEventHandler(Code.PhotoSwipe.EventTypes.onHide,
      function(e){
        idx = myPhotoSwipe.currentIndex;
        Code.PhotoSwipe.detatch(myPhotoSwipe);
        $.vegas('slideshow');
        $.vegas('jump', idx);
        $(document.body).click(goPhotoSwipe);
        event.stopPropagation();
      }
    );
    myPhotoSwipe.show(idx);
    return false;
  }  

  $(document.body).click(goPhotoSwipe);


//   $thumbnails.swipe({
//     swipeStatus: function(event, direction, distance, duration) {
//       console.log
//       if (direction == "right") {
//         jScrollPaneApi.scrollBy(-distance, 0, false);
//       } else {
//         jScrollPaneApi.scrollBy(distance, 0, false);
//       }
//       return false;
//     },
//     threshold: 0, triggerOnTouchEnd: false
//   });

  $pause.click(function() {
    $pause.hide();
  
    //$title.animate({bottom:'0px'});
    //$thumbnails.animate({top:'0px'});

    $.vegas('slideshow');

    return false;
  });

});
