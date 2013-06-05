/*******

	***	Link Fader by Cedric Dugas   ***
	*** Http://www.position-absolute.com ***
	
	You can use and modify this script for any project you want, 
	but please leave this comment as credit.
	
	With this script you can have beautiful fade in and fade out hover link.
	
	Just add the class linkFader at your <a> tag and it will fade, 
	user with javascript disable will still have the css hover.

	This script only work if you use the image replacement technique as it take 
	the background image of the <a> tag and play with the background position.
	
*****/

$(document).ready(function() {
	hoverOpacity.init()
});

hoverOpacity = {
	init : function(){
		$('a.linkFader').css({
			position:"relative",
			backgroundPosition:"0px 0px",
			cursor:"pointer"
		})
		$('a.linkFader').each(function(){
			
			spanFader = document.createElement('span');
			myBG = $(this).css("background-image")
			
			$(this).append(spanFader);
		
			myBG = $(this).css("background-image")
			spanWidth =  $(this).css("width")
			spanHeight =  $(this).css("height")
				
			$(this).find("span").css({
				backgroundImage:myBG,
				backgroundPosition:"bottom right",
				position:"absolute",
				display:"block",
				cursor:"pointer",
				top:"0px",
				left:"0px",
				width:spanWidth,
				height:spanHeight,
				opacity:0,
				visibility:"visible"
			})
		})
		$("a.linkFader").hover(function () {
			$(this).find("span").stop()
			$(this).find("span:not(:animated)").animate({opacity: 1}, 300)
		},
		function () {
			$(this).find("span").animate({opacity: 0},250)
		});
	}
}