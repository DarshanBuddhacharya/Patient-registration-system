const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});

$(".profile .icon_wrap").click(function(){
  $(this).parent().toggleClass("active");
  $(".notifications").removeClass("active");
  if (($(e.target).closest('.profile').length == 0) && ($(e.target).closest('.profile').length == 0)){
	  $(".profile").removeClass("active");
  }
});

$(".notifications .icon_wrap").click(function(){
  $(this).parent().toggleClass("active");
   $(".profile").removeClass("active");
});


//  $(document).on('click', function (e) {
//     if (($(e.target).closest('#menu').length == 0) && ($(e.target).closest('#open_menu').length == 0)) {
//       if (isMenuOpen == true) {
//         isMenuOpen = false;
//         $("#menu").hide();
//       }
//     }
//   });
