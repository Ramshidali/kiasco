$(".spotlight-slider").slick({
	dots: false,
	infinite: true,
	speed: 3000,
	slidesToShow: 1,
	slidesToScroll: 1,
	autoplay: true,
	autoplaySpeed: 2000,
});
$(".cancel-modal-wrapper div.top-rate span").click(function () {
	$(".cancel-modal-pop").hide();
});

// review stars
$(function () {
	$("div.star-rating > s, div.star-rating-rtl > s").on("click", function (e) {
		var numStars = $(e.target).parentsUntil("div").length + 1;
		// alert(numStars + (numStars == 1 ? " star" : " stars!"));
		console.log(numStars);
		console.log(numStars + (numStars == 1 ? " star" : " stars!"));
		$("div.star-rating s").removeClass("rated");
		$(e.target).parentsUntil("div").addClass("rated");
		$(e.target).addClass("rated");
		// .children().parentsUntil("div")
	});
});
// rating-popup
function review_span(order_pk) {
	$(".modal-pop").toggleClass("is-visible");
	pro_pk = $("." + order_pk + "modal-toggle").attr("data-pro_pk");
	$("#id_pro_pk").val(pro_pk);
	console.log(pro_pk + "prooooooooooo pk");
}

// cancel order
function cancel_span(order_pk, pro_id) {
	console.log("hai");
	$(".cancel-modal-pop").toggleClass("is-visible");
	$("#order_pk").val(order_pk);
	$("#pro_pk").val(pro_id);
}

// mobile-menu
function MobileMenu() {
	let body = document.querySelector("body");
	$(".hamburger").click(function (e) {
		body.classList.toggle("active");
	});
	$(".overlay").click(() => {
		body.classList.remove("active");
	});
}
MobileMenu();
function hideMenu() {
	body.classList.remove("active");
}
function paymentMethod() {
	$(".payment-container .payment-box li").click(function () {
		$(".payment-container .payment-box li.active").toggleClass("active");
		$(this).addClass("active");
	});
}
paymentMethod();

// const expirationdate = document.getElementById("expirationdate");
// var expirationdate_mask = new IMask(expirationdate, {
//   mask: "MM{/}YY",
//   groups: {
//     YY: new IMask.MaskedPattern.Group.Range([0, 99]),
//     MM: new IMask.MaskedPattern.Group.Range([1, 12]),
//   },
// });
// product-size-adjuster
function size() {
	$("#product .txt-box .size span a").click(function () {
		$("#product .txt-box .size span a.active").removeClass("active");
		$(this).addClass("active");
	});
}
size();

// say-slider
// gallery slider
var length = $("#say-slider .card-s").length;
var width = $(document).width();

function MySlick2() {
	if (
		(width > 1280 && length > 2) ||
		(width > 640 && width <= 1280 && length > 1)
	) {
		$("#say-slider").slick({
			dots: false,
			infinite: true,
			speed: 3000,
			slidesToShow: 2,
			slidesToScroll: 1,
			autoplay: true,
			autoplaySpeed: 2000,
			responsive: [
				{
					breakpoint: 642,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1,
					},
				},
			],
		});
	}
}
MySlick2();

// gallery slider
var length = $("#gallery-slider .card").length;
var width = $(document).width();

function MySlick1() {
	if (
		(width > 1280 && length > 4) ||
		(width > 640 && width <= 1280 && length > 2) ||
		(width > 320 && width <= 640 && length > 1)
	) {
		$("#gallery-slider").slick({
			dots: false,
			infinite: true,
			speed: 3000,
			slidesToShow: 5,
			rows: 2,
			slidesToScroll: 1,
			autoplay: true,
			autoplaySpeed: 2000,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1,
					},
				},
				{
					breakpoint: 642,
					settings: {
						slidesToShow: 2,
						slidesToScroll: 1,
					},
				},
				{
					breakpoint: 480,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1,
					},
				},
			],
		});
	}
}
MySlick1();

// offer-slider
$(".image-box").slick({
	dots: true,
	infinite: true,
	speed: 300,
	slidesToShow: 1,
	slidesToScroll: 1,
	autoplay: true,
	autoplaySpeed: 2000,
	responsive: [
		{
			breakpoint: 1024,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
				infinite: true,
				dots: true,
			},
		},
		{
			breakpoint: 600,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
			},
		},
		{
			breakpoint: 480,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
			},
		},
	],
});

// item-slider

var length = $(".item-slider li").length;
var width = $(document).width();

function MySlick() {
	if (
		(width > 1280 && length > 4) ||
		(width > 640 && width <= 1280 && length > 2) ||
		(width > 320 && width <= 640 && length > 1)
	) {
		$(".item-slider").slick({
			dots: false,
			infinite: true,
			speed: 300,
			slidesToShow: 4,
			slidesToScroll: 1,
			autoplay: true,
			autoplaySpeed: 2000,
			responsive: [
				{
					breakpoint: 1024,
					settings: {
						slidesToShow: 3,
						slidesToScroll: 1,
					},
				},
				{
					breakpoint: 642,
					settings: {
						slidesToShow: 2,
						slidesToScroll: 1,
					},
				},
				{
					breakpoint: 480,
					settings: {
						slidesToShow: 1,
						slidesToScroll: 1,
					},
				},
			],
		});
	}
}

MySlick();
// login
function login() {
	$("li.signin").click(function () {
		document.body.classList.toggle("login");
		$(".login-page .signup-box").css("display", "block");

		$(".login-page .login-box p a").click((e) => {
			$(".login-page .signup-box").css("display", "block");
			$(".login-page .login-box").css("display", "none");
			e.stopPropagation();
		});
	});
}
login();

// autofill-otp
$(".inputs").keyup(function () {
	if (this.value.length == this.maxLength) {
		$(this).next(".inputs").focus();
	}
});

// function wishlist() {
// 	$(".list-box .content-box li .text-box .name i").click(() => {
// 		icon.classList.toggle("fas");
// 	});
// }
// wishlist();

// sticky-header
window.onscroll = function () {
	headerFunction();
};

var body = document.body;
var sticky = body.offsetTop;

function headerFunction() {
	if (window.pageYOffset > 100) {
		body.classList.add("sticky");
	} else {
		body.classList.remove("sticky");
	}
}

// drop-down-menu
function dropDown() {
	$("header li.user").on("click", function () {
		$("header .right-box .drop-down").toggleClass("active");
	});
}
dropDown();
// $(document).on("click", function (e) {
//   if ($(e.target).is("header .right-box .drop-down.active") == false) {
//     $("header .right-box .drop-down").removeClass("active");
//   }
// });

function mobiDrop() {
	$("header li.user").click(() => {
		$("header .mobile-container .drop-down").toggleClass("active");
	});
}
mobiDrop();

// activating nav-menu elements
$("#spotlight .container-box .detials-box li a").click(function () {
	$("#spotlight .container-box .detials-box li a.active").removeClass(
		"active"
	);
	$(this).addClass("active");
});
// activating drop-menu elements
$("header .right-box .drop-down span a").click(function () {
	$("header .right-box .drop-down span a.active").removeClass("active");
	$(this).addClass("active");
});

//   revealing animation while scrolling
new WOW().init();

// gender-edit-profile
$("#spotlight .edit-page .gender-box a").click(() => {
	$("#spotlight .edit-page .gender-box a").toggleClass("active");
	$(this).addClass("active");
});

// closer
$("section.container-otp .head .close").click(() => {
	$("section.all-order").removeClass("active");
	$("section.container-otp").removeClass("active");
	$("section.otp-verification").removeClass("active");
	$("section.number-update").removeClass("active");
});
$("section.success .closer-head").click(() => {
	$("section.all-order").removeClass("active");
	$("section.container-otp").removeClass("active");
	$("section.otp-verification").removeClass("active");
	$("section.number-update").removeClass("active");
	$("section.success").removeClass("active");
});
// change-password-pop-up
$("#spotlight .edit-page .password-change").click(() => {
	$("section.change-password").addClass("active");
	$("section.all-order").addClass("active");
});
// $("section.change-password .button").click(() => {
// 	$("section.password-success").addClass("active");
// 	$("section.change-password").removeClass("active");
// });
$(".head .close").click(() => {
	$("section.change-password").removeClass("active");
	$("section.all-order").removeClass("active");
	$("section.password-success").removeClass("active");
	window.location.reload();
});
$("section.change-password .cancel").click(() => {
	$("section.change-password").removeClass("active");
	$("section.all-order").removeClass("active");
	window.location.reload();
});

// country-mobile-number-selector
// function country() {
// 	var input = document.querySelector("#phone");
// 	window.intlTelInput(input, {
// 		initialCountry: "auto",
// 		separateDialCode: "true",
// 	});
// 	iti.setCountry("india");
// }
// country();

// Selecting the input element and get its value
$(".login-page .signup-box .signup").click(function () {
	var inputVal = document.getElementById("mobile_number").value;
	$(".login-page .signup-detail .verify p small").html(inputVal);
	$(".login-page .mobile-otp span .number").html(inputVal);
	console.log(inputVal);
});

//  for-adding-more-address
$("#addAddress").click(function () {
	$(".add-address").addClass("active");
});

$(".close-address").click(function () {
	$(".add-address").removeClass("active");
	window.location.reload();
});

// product-detials-slider
var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
	showSlides((slideIndex += n));
}

function currentSlide(n) {
	showSlides((slideIndex = n));
}

function showSlides(n) {
	var i;
	var slides = document.getElementsByClassName("mySlides");
	var dots = document.getElementsByClassName("demo");
	if (n > slides.length) {
		slideIndex = 1;
	}
	if (n < 1) {
		slideIndex = slides.length;
	}
	for (i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	for (i = 0; i < dots.length; i++) {
		dots[i].className = dots[i].className.replace(" active", "");
	}
	// slides[slideIndex - 1].style.display = "block";
	// dots[slideIndex - 1].className += " active";
}
showSlides();

// function qty() {
// 	var counterValue = document.querySelector("#counter-value");
// 	var counterIncrement = document.querySelector("#counter-increment");
// 	var counterDecrement = document.querySelector("#counter-decrement");
// 	var count = 1;
// 	this.counterIncrement.addEventListener("click", () => {
// 		if (count < 5) {
// 			this.count++;
// 			this.counterValue.setAttribute("value", count);
// 		}
// 	});

// 	this.counterDecrement.addEventListener("click", () => {
// 		if (count > 1) {
// 			this.count--;
// 			this.counterValue.setAttribute("value", count);
// 		}
// 	});
// }
