$(document).ready(function(){
  $('.vet-status').click(function(){
    if( $(this).hasClass('vet-status--unvetted') ) { 
      $(this).removeClass('vet-status--unvetted');
      $(this).addClass('vet-status--vetted');
      $(this).html('<span class="icon-vetted"></span>Vetted');
    } else if ( $(this).hasClass('vet-status--vetted') ) {
      $(this).removeClass('vet-status--vetted');
      $(this).addClass('vet-status--unvetted');
      $(this).html('Unvetted');
    }
  });
});