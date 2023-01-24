$("#submit_phone").click(function (e) {
	e.preventDefault();

	var timeLeft = 30;
	var elem = document.getElementById("some_div");
	var timerId = setInterval(countdown, 1000);

	function countdown() {
		if (timeLeft == -1) {
			clearTimeout(timerId);
			doSomething();
		} else {
			elem.innerHTML = timeLeft + " sec";
			timeLeft--;
		}
	}

	function doSomething() {
		$(".resend .resend_button").css("display", "block");
	}

	phone = $("#mobile_number").val();
	var filter = /^\d*(?:\.\d{1,2})?$/;
	filter_test = filter.test(phone);
	console.log(filter_test);

	$("#required_text_phone").css({
		display: "none",
	});

	if (phone.length === 0) {
		$("#required_text_phone").css({
			display: "block",
		});
	} else if (filter_test == false) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html("enter correct phone number");
	} else if (phone.length > 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number greater than 10"
		);
	} else if (phone.length < 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number less than 10"
		);
	} else {
		next_url = $(this).attr("data-next-url");
		url = $(this).attr("data-url");

		console.log(phone);

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
			},

			success: function (data) {
				if (data["status"] == "true") {
					$(".login-page .mobile-otp").addClass("active");
					$(".login-page .signup-box").css("display", "none");

					$(".number").html(phone);
					$("#otp_validation").attr("data-url", next_url);

				}

				if (data["status"] == "6001") {
					if (data["condition_status"] == "phone_already_exists") {
						$("#required_text_phone").css({
							display: "block",
						});
						$("#required_text_phone").html(data["message"]);
					}
				}
			},

			error: function (data) {},
		});
	}
});

$("#otp_validation").click(function (e) {
	e.preventDefault();
	$("#required_text_otp").css({
		display: "none",
	});

	if (
		$("#otp_one").val().length === 0 &&
		$("#otp_two").val().length === 0 &&
		$("#otp_three").val().length === 0 &&
		$("#otp_four").val().length === 0
	) {
		$("#required_text_otp").css({
			display: "block",
		});
	} else {
		phone = $(".number").html();
		otp_one = $("#otp_one").val();
		otp_two = $("#otp_two").val();
		otp_three = $("#otp_three").val();
		otp_four = $("#otp_four").val();

		url = $(this).attr("data-url");

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
				otp_one: otp_one,
				otp_two: otp_two,
				otp_three: otp_three,
				otp_four: otp_four,
			},

			success: function (data) {
				if (data["status"] == "true") {
					if (data["next_action"] == "registration_page") {
						$(".login-page .signup-detail").addClass("active");
						$(".login-page .mobile-otp").css("display", "none");

						$(".number").html(phone);
					}
					if (data["next_action"] == "exit") {
						location.reload();
					}

				}

				if (data["status"] == "false") {
					if (data["condition_status"] == "not_match") {
						$("#required_text_otp").css({
							display: "block",
						});
						$("#required_text_otp").html(data["message"]);
					}
				}
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});

// signup password checking
// $("#signup_password").keyup(function (e) {
// 	e.preventDefault();
// 	password = $("#signup_password").val();
// 	var upper_valid, char_valid, special_valid, num_valid;
// 	var special = new RegExp(/[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/);
// 	var upper = new RegExp(/[A-Z]/);
// 	var numeric = new RegExp(/\d/);

// 	if (upper.test(password) == true) {
// 		$("#upper").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		upper_valid = true;
// 	}
// 	if (upper.test(password) == false) {
// 		$("#upper").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		upper_valid = false;
// 	}
// 	if (special.test(password) == true) {
// 		$("#special").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		special_valid = true;
// 	}
// 	if (special.test(password) == false) {
// 		$("#special").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		special_valid = false;
// 	}
// 	if (numeric.test(password) == true) {
// 		$("#numeric").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		num_valid = true;
// 	}
// 	if (numeric.test(password) == false) {
// 		$("#numeric").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		num_valid = false;
// 	}
// 	if (password.length >= 8) {
// 		$("#charecter").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		char_valid = true;
// 	}
// 	if (password.length < 8) {
// 		$("#charecter").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		char_valid = false;
// 	}
// 	if (password.length == 0) {
// 		$("#special").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		char_valid = false;
// 	}
// 	if (upper_valid && num_valid && special_valid && char_valid) {
// 		$("#signup").addClass("active");
// 	} else {
// 		$("#signup").removeClass("active");
// 	}
// 	console.log(upper_valid, "upper_valid");
// 	console.log(num_valid, "num_valid");
// 	console.log(special_valid, "special_valid");
// 	console.log("**************************");
// });

// signup submit

$("#signup").click(function (e) {
	e.preventDefault();
	console.log("entered");
	$("#required_text_name").css({
		display: "none",
	});
	$("#required_text_email").css({
		display: "none",
	});
	$("#required_text_password").css({
		display: "none",
	});
	$("#required_text_gender").css({
		display: "none",
	});
	// required text
	if ($("#name").val().length === 0) {
		$("#required_text_name").css({
			display: "block",
		});
	} else if ($("#signup_email").val().length === 0) {
		$("#required_text_email").css({
			display: "block",
		});
	} else if ($(".genders").val().length === 0) {
		$("#required_text_gender").css({
			display: "block",
		});
	} else {
		phone = $(".number").html();
		user_name = $("#name").val();
		email = $("#signup_email").val();
		gender = $("input[name='genders']:checked").val();
		url = $(this).attr("data-url");

		console.log(url)
		// console.log(email)
		// console.log(password)



		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
				user_name: user_name,
				email: email,
				gender: gender,
			},

			success: function (data) {
				c_status = data["condition_status"];
				message = data["message"];

				// console.log(c_status);
				// console.log(message);

				if (data["status"] == "true") {
					location.reload();
				}
				if (data["status"] == "6001") {
					if (
						data["condition_status"] == "phone_already_exists"
					) {
						$("#required_text_name").css({ display: "block" });
						$("#required_text_name").html(message);
					}
					if (
						data["condition_status"] == "email_already_exists"
					) {
						$("#required_text_email").css({ display: "block" });
						$("#required_text_email").html(message);
					}
				}
				// $(".login-page .signup-detail").addClass("active");
				// $(".login-page .signup-detail").css("display", "none");
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});

// check email is exists and email is entered
// $(".forgot").click(function (e) {
// 	e.preventDefault();
// 	console.log("enterd");

// 	email = $("#login_email").val();
// 	url = $(this).attr("data-url");

// 	if (email.length <= 0) {
// 		$("#required_text_email").css("display", "block");
// 		$("#required_text_email").html("Enter E-mail ID");
// 	} else {
// 		$.ajax({
// 			type: "GET",
// 			url: url,
// 			dataType: "json",
// 			data: {
// 				email: email,
// 			},

// 			success: function (data) {
// 				c_status = data["condition_status"];
// 				message = data["message"];

// 				console.log(c_status);
// 				console.log(message);

// 				if (data["status"] == "true") {
// 					$(".login-page .email-otp").addClass("active");
// 					$(".login-page .email-otp").css("display", "block");
// 					$("#email_otp_validation").attr("data-email", email);

// 					$(".login-page .login-box").css("display", "none");

// 					$(".number").html(email);
// 				}

// 				if (data["status"] == "false") {
// 					$("#required_text_email").css("display", "block");
// 					$("#required_text_email").html(message);
// 				}
// 			},

// 			error: function (data) {
// 				//    console.log("errrorrrr")
// 			},
// 		});
// 	}
// });

// forgot password checking
// $("#forgot-new-password").keyup(function (e) {
// 	e.preventDefault();

// 	password = $("#forgot-new-password").val();
// 	var upper_valid, char_valid, special_valid, num_valid;
// 	var special = new RegExp(/[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/);
// 	var upper = new RegExp(/[A-Z]/);
// 	var numeric = new RegExp(/\d/);

// 	if (upper.test(password) == true) {
// 		$(".upper").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		upper_valid = true;
// 	}
// 	if (upper.test(password) == false) {
// 		$(".upper").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		upper_valid = false;
// 	}
// 	if (special.test(password) == true) {
// 		$(".special").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		special_valid = true;
// 	}
// 	if (special.test(password) == false) {
// 		$(".special").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		special_valid = false;
// 	}
// 	if (numeric.test(password) == true) {
// 		$(".numeric").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		num_valid = true;
// 	}
// 	if (numeric.test(password) == false) {
// 		$(".numeric").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		num_valid = false;
// 	}
// 	if (password.length >= 8) {
// 		$(".charecter").css({
// 			"background-color": "green",
// 			color: "#fff",
// 		});
// 		char_valid = true;
// 	}
// 	if (password.length < 8) {
// 		$(".charecter").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		char_valid = false;
// 	}
// 	if (password.length == 0) {
// 		$(".special").css({
// 			"background-color": "#fff",
// 			color: "black",
// 		});
// 		char_valid = false;
// 	}
// 	if (upper_valid && num_valid && special_valid && char_valid) {
// 		$("#forgot-pass-submit").attr("data-is_active", "active");
// 	} else {
// 		$("#forgot-pass-submit").attr("data-is_active", "");
// 	}
// 	console.log(upper_valid, "upper_valid");
// 	console.log(num_valid, "num_valid");
// 	console.log(special_valid, "special_valid");
// 	console.log("**************************");
// });

// forgot password submit
// $("#forgot-pass-submit").click(function (e) {
// 	e.preventDefault();
// 	email = $("#email_id").val();
// 	password = $("#forgot-new-password").val();
// 	c_password = $("#forgot_c_password").val();
// 	url = $(this).attr("data-url");

// 	console.log("emmmmmmmmmmaaaaaaail" + email);

// 	if (password.length <= 0) {
// 		$("#required_text_f_password").css({
// 			display: "block",
// 		});
// 	} else {
// 		$("#required_text_f_password").css({
// 			display: "none",
// 		});
// 	}
// 	if (c_password.length <= 0) {
// 		$("#required_text_f_c_password").css({
// 			display: "block",
// 		});
// 	} else {
// 		$("#required_text_f_c_password").css({
// 			display: "none",
// 		});
// 	}

// 	if ($("#forgot-pass-submit").attr("data-is_active") == "active") {
// 		console.log("active+=========================");

// 		if (password == c_password) {
// 			console.log("ajaaaaxx");

// 			$.ajax({
// 				type: "GET",
// 				url: url,
// 				dataType: "json",
// 				data: {
// 					email: email,
// 					password: password,
// 					c_password: c_password,
// 				},

// 				success: function (data) {
// 					c_status = data["condition_status"];
// 					message = data["message"];

// 					console.log(c_status);
// 					console.log(message);

// 					if (data["status"] == "true") {
// 						$(".login-page .sett-paasword-box").css(
// 							"visibility",
// 							"hidden"
// 						);
// 						$("body").removeClass("login");

// 						$("#profile-sweet-message").html(message);
// 						$(".tick-box #title").html(title);

// 						$("#forgot_success").addClass("active");
// 						$("#forgot_success").css("display", "block");
// 					}

// 					if (data["status"] == "false") {
// 						$("#required_text_email").css("display", "block");
// 						$("#required_text_email").html(message);
// 					}
// 				},

// 				error: function (data) {
// 					//    console.log("errrorrrr")
// 				},
// 			});
// 		} else {
// 			console.log("not equal	++++++=======================");
// 			$("#required_text_f_c_password").css({
// 				display: "block",
// 			});
// 			$("#required_text_f_c_password").html("Password not match");
// 		}
// 	} else {
// 		$("#required_text_f_password").css({
// 			display: "block",
// 		});
// 		$("#required_text_f_password").html("Enter password currect format");
// 	}
// });

// closer

$("section.success .f-pass-closer-head").click(() => {
	$("section.all-order").removeClass("active");
	$("section.container-otp").removeClass("active");
	$("section.otp-verification").removeClass("active");
	$("section.number-update").removeClass("active");
	$("section.success").removeClass("active");
	// $(".login-page").hide()

	// console.log("+++++++++" + "sign innnnnnnnnn");
	signin();
});

// email otp validation checking
$("#email_otp_validation").click(function (e) {
	e.preventDefault();
	// console.log("enterdddd");
	$("#required_text_otp").css({
		display: "none",
	});

	if (
		$("#frgt_otp_one").val() &&
		$("#frgt_otp_two").val() &&
		$("#frgt_otp_three").val() &&
		$("#frgt_otp_four").val().length === 0
	) {
		// console.log("ifffffff");

		$("#required_text_otp").css({
			display: "block",
		});
	} else {
		// console.log("else");

		email = $(".number").html();
		otp_one = $("#frgt_otp_one").val();
		otp_two = $("#frgt_otp_two").val();
		otp_three = $("#frgt_otp_three").val();
		otp_four = $("#frgt_otp_four").val();

		// console.log(otp_one);
		// console.log(otp_two);
		// console.log(otp_three);
		// console.log(otp_four);

		url = $(this).attr("data-url");

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				email: email,
				otp_one: otp_one,
				otp_two: otp_two,
				otp_three: otp_three,
				otp_four: otp_four,
			},

			success: function (data) {
				// console.log(data["status"]);
				if (data["status"] == "true") {
					$(".login-page .sett-paasword-box").addClass("active");
					$(".login-page .sett-paasword-box").css("display", "block");
					$(".login-page .email-otp").css("display", "none");

					$("#email_id").attr("value", email);
				}

				if (data["status"] == "false") {
					if (data["condition_status"] == "not_match") {
						$("#required_text_otp").css({
							display: "block",
						});
						$("#required_text_otp").html(data["message"]);
					}
				}
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});


function isEmail(email) {
	var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
  }


$("#customer_login").click(function (e) {
	e.preventDefault();
	email = $("#login_email").val();
	password = $("#login_password").val();

	check_mail = IsEmail(email);

	$("#invalid_email").css({
		display: "none",
	});
	$("#required_text_email").css({
		display: "none",
	});
	$("#required_text_password").css({
		display: "none",
	});

	// required text
	if (email.length === 0) {
		// alert('Enter your email and password!');
		$("#required_text_email").css({
			display: "block",
		});
		// console.log("emai legthhhhhhhhhhhhhhhhhh")
	} else if (check_mail == false) {
		// console.log("check iffffffff")
		$("#invalid_email").css({
			display: "block",
		});
		// $('#invalid_email').block();
		return false;
	} else if (password.length === 0) {
		$("#required_text_password").css({
			display: "block",
		});
	} else {
		url = $(this).attr("data-url");
		// console.log(email)
		// console.log(password)

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				email: email,
				password: password,
			},

			success: function (data) {
				if (data["status"] == "true") {
					location.reload();
				}
				if (data["status"] == "false") {
					c_status = data["condition_status"];
					message = data["message"];
					console.log(c_status);
					console.log(message);

					if (data["condition_status"] == "not_match") {
						$("#required_text_password").css({ display: "block" });
						$("#required_text_password").html(message);
					}

					if (data["condition_status"] == "password_not_match") {
						$("#required_text_password").css({ display: "block" });
						$("#required_text_password").html(message);
					}

					if (data["condition_status"] == "username_not_found") {
						$("#required_text_password").css({ display: "block" });
						$("#required_text_password").html(message);
					}
				}
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});

$(".add-to-wishlist").click(function (e) {
	e.preventDefault();

	product = $(this).attr("data-product");
	url = $(this).attr("data-url");
	t_his = $(this);

	add_wishlist_ajax(product, url, t_his);
});

function add_wishlist_ajax(product, url, t_his) {
	// console.log(product)
	// console.log(url)
	// console.log(t_his)

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			product: product,
		},

		success: function (data) {
			t_his.addClass("far");

			console.log(data["status"]);
			if (data["status"] == "added") {
				t_his.removeClass("far");
				t_his.addClass("fa");
				// t_his.animate({transform: "scale(1)"}, 500, 'linear');
				t_his.toggleClass("wishlist-fill");
				$(".product-button-box").load();
			} else if (data["status"] == "removed") {
				// console.log("removed-------------------");
				t_his.removeClass("fa");
				t_his.addClass("far");
				// t_his.css({ color: "#327af8" });
				$(".product-button-box").load();
			} else if (data["status"] == "nouser") {
				// console.log("no user ==============");
				document.body.classList.toggle("login");
				$(".login-page .login-box").css("display", "block");
				$(".login-page .signup-box").css("display", "block");
				// $(".login-page .login-box p a").click(() => {
				// 	$(".login-page .login-box").css("display", "none");
				// });
				console.log("hiii")
			}

			// window.location.reload();
		},

		error: function (data) {
			console.log("errrorrrr");
		},
	});
}

$(".signin").click(function () {
	signin();
});

function signin() {
	// console.log("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu");
	document.body.classList.toggle("login");
	$(".login-page .login-box").css("display", "block");

	$(".login-page .login-box p a").click(() => {
		$(".login-page .signup-box").css("display", "block");
		$(".login-page .login-box").css("display", "none");
	});
}

$(".select-varient").click(function (e) {
	e.preventDefault();
	// get pk from varient
	product_varient = $(this).attr("data-varient");
	// add to button data-varient
				// console.log(message);
	$(".add-cart").attr("data-varient", product_varient);
});

// single product's select variant and set first varient id select
$(document).ready(function () {
	$(".select-varient").first().addClass("active");
	variant = $(".select-varient").first().attr("data-varient");
	$(".add-cart").attr("data-varient", variant);

	selectedvarient(variant)
});

$(".add-cart").click(function (e) {
	e.preventDefault();

	varient = $(this).attr("data-varient");
	url = $(this).attr("data-url");
	t_his = $(this);

	add_cart_ajax(varient, url, t_his);
});

function add_cart_ajax(varient, url, t_his) {
	// console.log(varient);
	// console.log(url);
	// console.log(t_his);

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			varient: varient,
		},

		success: function (data) {
			// console.log(data["status"]);
			if (data["status"] == "selectVarient") {
				// console.log("no varient ==============");
			} else if (data["status"] == "nouser") {
				// console.log("no user ==============");
				document.body.classList.toggle("login");
				$(".login-page .login-box").css("display", "block");
				$(".login-page .signup-box").css("display", "block");
				// $(".login-page .login-box p a").click(() => {
				// 	$(".login-page .login-box").css("display", "none");
				// });
				console.log("hiii")
			} else if (data["status"] == "added") {
				// console.log("added-------------------");
				location.reload();
			} else if (data["status"] == "removed") {
				// console.log("removed-------------------");
				location.reload();
			}
		},

		error: function (data) {
			console.log("errrorrrr");
		},
	});
}

$("#chech-pincode").click(function (e) {
	e.preventDefault();
	// get pk from varient
	pincode = $("#pincode").val();
	url = $(this).attr("data-url");

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			pincode: pincode,
		},

		success: function (data) {
			// console.log(data["status"]);
			if (data["status"] == "available") {
				// console.log("true-------------------");
				date = data["delivery_date"];
				$("#cash_on_delivery").css("display", "none");
				// $("#delivery_date").children("span").remove();
				// $("#delivery_date").removeData()
				console.log(data["is_cod"]);

				$("#delivery_date").html(
					"get it buy " +
						date +
						"<span>" +
						"<i class='fas fa-check-circle'></i>" +
						"</span>"
				);

				if (data["is_cod"] == "True") {
					$("#cash_on_delivery").css(
						"display",
						"flex" & "color",
						"green"
					);
					$("#cash_on_delivery").html(
						"COD Available " +
							"<span>" +
							"<i class='fas fa-check-circle'></i>" +
							"</span>"
					);
				}
			} else if (data["status"] == "not_available") {
				console.log("false-------------------");
				$("#delivery_date").html(
					"Delivery Not Available on this Pincode"
				);
			}
		},

		error: function (data) {
			console.log("errrorrrr");
		},
	});
});

// unit price count
$(document).ready(function () {
	id = $(".varient_pk").attr("data-varient");
	price = $(".price-hide").val();
	var qty = $("#counter-value").val();
	u_price = qty * price;
	$("." + id + "cart-unit").html("₹ " + u_price);
	// console.log(id)
	// console.log(price)
	// console.log(u_price)
});

// increment and decrement qty
// decrement
function counter_decrement(id) {
	// get pk from varient
	console.log("decrease====================");
	console.log(id);

	var qty = $(`#${id}counter-value`);
	var qty_value = parseInt(qty.val(), 10);

	console.log("qty-----------", qty.length);
	var url = $("#" + id + "counter-decrement").attr("href");

	if (qty_value - 1 == 0) {
		console.log("yesy in in");
		id = qty.attr("data-id");
		url = qty.attr("empty");
		console.log(id, "-id----", url, "---url----");
		remove_from_ajax(id, url);
	} else if (qty_value != 1) {
		// qty_value = parseInt(qty_value, 10) - 1;
		qty_value -= 1;
		console.log(qty_value + "-------baa----------");
		counter_decremet_ajax(id, url);
	}
}

function counter_decremet_ajax(id, url) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			product_variant: id,
		},

		success: function (data) {
			if (data["status"] == "updated") {
				console.log(data["status"]);
				console.log(data["total_price"]);
				$("#" + id + "counter-value").val(data["qty"]);
				$("." + id + "unit_price").html("₹ " + data["unit_price"]);
				$("#total_price").html("₹ " + data["total_price"]);
				$("#" + id + "qty_requirements").css("display", "none");
			}
			//  console.log('.'+id+'class'$('.'+id+'cart-unit').html("₹ " + data['price']))
			//  console.log(data['price'])
			// location.reload();
		},

		error: function (data) {
			var title = "An error occurred";
			var message = "An error occurred. Please try again later.";
			// swal(title, message, "error");
		},
	});
}

// increment

function counter_increment(id) {
	// e.preventDefault();
	// get pk from varient
	console.log("increment====================");
	var qty = document.getElementById("counter-value");

	var url = $("#" + id + "counter-increment").attr("href");

	counter_increment_ajax(id, url);
}

function counter_increment_ajax(id, url) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			product_variant: id,
		},

		success: function (data) {
			console.log(data["status"]);

			if (data["status"] == "updated") {
				$("#" + id + "counter-value").val(data["qty"]);
				$("." + id + "unit_price").html("₹ " + data["unit_price"]);
				$("#total_price").html("₹ " + data["total_price"]);
			}
			if (data["status"] == "greaterthan") {
				var message = data["message"];

				$("#" + id + "qty_requirements").html(message);
				$("#" + id + "qty_requirements").css("display", "block");
			}
		},

		error: function (data) {
			var title = "An error occurred";
			var message = "An error occurred. Please try again later.";
			// swal(title, message, "error");
		},
	});
}

// remove from cart

$(".remove-cart").click(function (e) {
	e.preventDefault();
	// get pk from varient
	console.log("remove====================");
	let id = $(this).attr("data-varient");
	var url = $(this).attr("data-url");

	remove_cart_from_ajax(id, url);
});

function remove_cart_from_ajax(id, url) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			varient: id,
		},

		success: function (data) {
			console.log(data["action"]);
			if (data["action"] == "removed") {
			}

			window.location.reload();
		},

		error: function (data) {
			var title = "An error occurred";
			var message = "An error occurred. Please try again later.";

			$("#profile-sweet-message").html(message);
			$(".tick-box #title").html(title);

			$("section.all-order").addClass("active");
			$("section.success").addClass("active");
			$("section.number-update").removeClass("active");
		},
	});
}

$(".profile-save-button").click(function (e) {
	e.preventDefault();

	c_name = $("#profile-name").val();
	email = $("#profile-email").val();
	gender = $(".gender-box .active").attr("data-gender");

	console.log(gender + "==================");

	var url = $(this).attr("data-url");

	// if (new_phone.length === 0) {
	// 	$("#required_text_phone").css({
	// 		display: "block",
	// 	});
	// } else if (new_phone.length > 10) {
	// 	$("#required_text_phone").css({
	// 		display: "block",
	// 	});
	// 	$("#required_text_phone").html(
	// 		"Enter a valid number, seens like you entered phone number greaterthan 10"
	// 	);
	// } else if (new_phone.length < 10) {
	// 	$("#required_text_phone").css({
	// 		display: "block",
	// 	});
	// 	$("#required_text_phone").html(
	// 		"Enter a valid number, seens like you entered phone number lessthan 10"
	// 	);
	// } else {
	url = $(this).attr("data-url");

	change_profile_ajax(c_name, email, gender, url);
});

function change_profile_ajax(c_name, email, gender, url) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			c_name: c_name,
			email: email,
			gender: gender,
		},

		success: function (data) {
			console.log(data["status"]);
			if (data["status"] == "success") {
				var title = "Successfull";
				var message = "your profile has been updated succesfully";

				$("#profile-sweet-message").html(message);
				$(".tick-box #title").html(title);

				$("section.all-order").addClass("active");
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}
		},

		error: function (data) {
			if (data["status"] == "success") {
				var title = "An error occurred";
				var message = "An error occurred. Please try again later.";

				$("#profile-sweet-message").html(message);
				$(".tick-box #title").html(title);

				$("section.all-order").addClass("active");
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}
		},
	});
}

// change phone number from profile edit page

$("#change-phone").click(() => {
	new_phone = $("#profile-phone").val();
	url = $("#change-phone").attr("data-url");

	console.log(url);

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",

		success: function (data) {
			console.log(data["status"]);
			if (data["status"] == "true") {
				$("section.all-order").addClass("active");
				$("section.otp-verification").addClass("active");

				$("#sent-phone-number").html(data["phone"]);
				$("#phone-varify-button").attr("data-phone", new_phone);
			}
		},

		error: function (data) {
			if (data["status"] == "success") {
				var title = "An error occurred";
				var message = "An error occurred. Please try again later.";

				$("#profile-sweet-message").html(message);
				$(".tick-box #title").html(title);

				$("section.all-order").addClass("active");
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}
		},
	});
});

$("#phone-varify-button").click(function (e) {
	e.preventDefault();
	$("#required_text_otp").css({
		display: "none",
	});

	if (
		$("#phone-otp-one").val().length === 0 &&
		$("#phone-otp-two").val().length === 0 &&
		$("#phone-otp-three").val().length === 0 &&
		$("#phone-otp-four").val().length === 0
	) {
		$("#required_text_otp").css({
			display: "block",
		});
	} else {
		phone = $("#sent-phone-number").html();
		new_phone = $("#phone-varify-button").attr("data-phone");
		otp_one = $("#phone-otp-one").val();
		otp_two = $("#phone-otp-two").val();
		otp_three = $("#phone-otp-three").val();
		otp_four = $("#phone-otp-four").val();

		url = $(this).attr("data-url");
		change_url = $(this).attr("data-change_url");

		// console.log(otp_one);
		// console.log(otp_two);
		// console.log(otp_three);
		// console.log(otp_four);
		// console.log(change_url);
		// console.log(new_phone);
		// console.log(url,"----------------url");

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
				otp_one: otp_one,
				otp_two: otp_two,
				otp_three: otp_three,
				otp_four: otp_four,
			},

			success: function (data) {
				// console.log(data);
				// console.log(data["status"]);
				// console.log(data["phone"]);
				// console.log("truuuuuuuuuuuuuuuu");

				if (data["status"] == "true") {
					change_phone_number(new_phone, change_url);
				}

				if (data["status"] == "false") {
					// console.log("falseeeeeeeeee");

					if (data["condition_status"] == "not_match") {
						$("#required_text_otp").css({
							display: "block",
						});
						$("#required_text_otp").html(data["message"]);
					}
				}
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});

function change_phone_number(new_phone, change_url) {
	console.log("into change passsword");
	$.ajax({
		type: "GET",
		url: change_url,
		dataType: "json",
		data: {
			new_phone: new_phone,
		},

		success: function (data) {
			if (data["status"] == "true") {
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}

			if (data["status"] == "false") {
				if (data["condition_status"] == "not_match") {
					$("#required_text_otp").css({
						display: "block",
					});
					$("#required_text_otp").html(data["message"]);
				}
			}
		},

		error: function (data) {
			//    console.log("errrorrrr")
		},
	});
}

// $("section.otp-verification .button").click(() => {
// 	$("section.number-update").addClass("active");
// 	$("section.otp-verification").removeClass("active");
// });

// $("section.number-update .button").click(() => {
// 	$("section.success").addClass("active");
// 	$("section.number-update").removeClass("active");
// });

$("#new-password").keyup(function (e) {
	e.preventDefault();

	old_password = $("#old-password").val();
	new_password = $("#new-password").val();
	c_password = $("#c-password").val();

	var upper_valid, char_valid, special_valid, num_valid;
	var special = new RegExp(/[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/);
	var upper = new RegExp(/[A-Z]/);
	var numeric = new RegExp(/\d/);

	if (upper.test(new_password) == true) {
		$("section.change-password .suggest #upper").css({
			background: "green",
			color: "#fff",
		});
		$("section.change-password .suggest #upper").addClass("active");
		upper_valid = true;
	}
	if (upper.test(new_password) == false) {
		$("section.change-password .suggest #upper").css({
			background: "#ffd4d6",
			color: "#c40000",
		});
		$("section.change-password .suggest #upper").removeClass("active");
		upper_valid = false;
	}
	if (special.test(new_password) == true) {
		$("section.change-password .suggest #special").css({
			background: "green",
			color: "#fff",
		});
		$("section.change-password .suggest #special").addClass("active");
		special_valid = true;
	}
	if (special.test(new_password) == false) {
		$("section.change-password .suggest #special").css({
			background: "#ffd4d6",
			color: "#c40000",
		});
		$("section.change-password .suggest #special").removeClass("active");
		special_valid = false;
	}
	if (numeric.test(new_password) == true) {
		$("section.change-password .suggest #numeric").css({
			background: "green",
			color: "#fff",
		});
		$("section.change-password .suggest #numeric").addClass("active");
		num_valid = true;
	}
	if (numeric.test(new_password) == false) {
		$("section.change-password .suggest #numeric").css({
			background: "#ffd4d6",
			color: "#c40000",
		});
		$("section.change-password .suggest #numeric").removeClass("active");
		num_valid = false;
	}
	if (new_password.length >= 8) {
		$("section.change-password .suggest #charecter").css({
			background: "green",
			color: "#fff",
		});
		$("section.change-password .suggest #charecter").addClass("active");
		char_valid = true;
	}
	if (new_password.length < 8) {
		$("section.change-password .suggest #charecter").css({
			background: "#ffd4d6",
			color: "#c40000",
		});
		$("section.change-password .suggest #charecter").removeClass("active");
		char_valid = false;
	}
	if (new_password.length == 0) {
		$("section.change-password .suggest #special").css({
			background: "#ffd4d6",
			color: "#c40000",
		});
		$("section.change-password .suggest #special").removeClass("active");
		char_valid = false;
	}

	// console.log(upper_valid,"upper_valid")
	// console.log(num_valid,"num_valid")
	// console.log(special_valid,"special_valid")
	// console.log(old_password,"old passs")
	// console.log("**************************")
});

$("#password-change-submit-button").click(function (e) {
	e.preventDefault();

	charecter = false;
	special = false;
	upper = false;
	numeric = false;

	old_password = $("#old-password").val();
	new_password = $("#new-password").val();
	c_password = $("#c-password").val(); //conform password

	// console.log(old_password,"---");
	// console.log(new_password);
	// console.log(upper);
	// console.log(numeric,"----");

	// console.log(upper);
	// console.log($("section.change-password .suggest #charecter").hasClass("active"),"check is active")
	// console.log(upper);

	if (old_password.length != 0 && new_password != 0 && c_password != 0) {
		if (
			$("section.change-password .suggest #charecter").hasClass("active")
		) {
			console.log((charecter = true + "char"));
			charecter = true;
		}
		console.log(
			$("section.change-password .suggest #special").hasClass("active")
		);
		if ($("section.change-password .suggest #special").hasClass("active")) {
			special = true;
		}
		console.log(
			$("section.change-password .suggest #upper").hasClass("active")
		);
		if ($("section.change-password .suggest #upper").hasClass("active")) {
			upper = true;
		}
		console.log(
			$("section.change-password .suggest #numeric").hasClass("active")
		);
		if ($("section.change-password .suggest #numeric").hasClass("active")) {
			numeric = true;
		}
		// console.log('----------------s');

		// console.log(charecter)
		// console.log(special)
		// console.log(upper)
		// console.log(numeric)

		if (charecter && special && upper && numeric) {
			console.log("insert from 1st if-----------------");

			if (old_password.length <= 0) {
				$("#old-password").css("border-color", "red");
				$("#old_password_text").html("*required field");
			} else if (new_password.length <= 0) {
				$("#new-password").css("border-color", "red");
				$("#new_password_text").html("*required field");
			} else if (c_password.length <= 0) {
				$("#c-password").css("border-color", "red");
				$("#c_password_text").html("*required field");
			} else {
				if (new_password == c_password) {
					var url = $(this).attr("data-url");

					$.ajax({
						type: "GET",
						url: url,
						dataType: "json",
						data: {
							old_password: old_password,
							new_password: new_password,
							c_password: c_password,
						},

						success: function (data) {
							console.log(data["status"]);
							if (data["status"] == "success") {
								var title = "Success";
								var message =
									"your password has been changed succesfully";

								$("#profile-sweet-message").html(message);
								$(".tick-box #title").html(title);

								$("section.all-order").addClass("active");
								$("section.success").addClass("active");
								$("section.number-update").removeClass(
									"active"
								);

								// window.location.replace("/")
								signin();
							}
							if (data["status"] == "false") {
								if (
									data["condition_status"] ==
									"old_password_not_match"
								) {
									$("#old-password").css(
										"border-color",
										"red"
									);
									$("#old_password_text").html(
										"*" + data["message"]
									);
								}

								if (
									data["condition_status"] ==
									"new_and_confirm_password_not_match"
								) {
									$("#c-password").css("border-color", "red");
									$("#c_password_text").html(
										"*" + data["message"]
									);
								}
							}
						},

						error: function (data) {
							if (data["status"] == "error") {
								var title = "An error occurred";
								var message =
									"An error occurred. Please try again later.";

								$("#profile-sweet-message").html(message);
								$(".tick-box #title").html(title);

								$("section.all-order").addClass("active");
								$("section.success").addClass("active");
								$("section.number-update").removeClass(
									"active"
								);
							}
						},
					});
				} else {
					$("#new-password").css("border-color", "red");
					$("#c-password").css("border-color", "red");
					$("#c_password_text").css("display", "block");
					$("#c_password_text").html("*confirm password not match");
				}
			}
		} else {
			$("#new-password").css("border-color", "red");
			$("#new_password_text").css("display", "block");
			$("#new_password_text").html("*fill password currectly");
		}
	} else {
		$("#old-password").css("border-color", "red");
		$("#old_password_text").css("display", "block");
		$("#old_password_text").html("*required field");

		$("#new-password").css("border-color", "red");
		$("#new_password_text").css("display", "block");
		$("#new_password_text").html("*required field");

		$("#c-password").css("border-color", "red");
		$("#c_password_text").css("display", "block");
		$("#c_password_text").html("*required field");
	}
});

function default_address(id) {
	// console.log("default addressssss");
	address_pk = $("#" + id).attr("data-pk");
	// url = $('#'+id).attr("data-url");
	// console.log(address_pk);
	$("#cart_address_btn").attr("data-address_pk", address_pk);
}

// edit address
$("#edit_address_button").click(function (e) {
	var url = $(this).attr("data-url");
	var c_name = $(this).attr("data-name");
	var phone = $(this).attr("data-phone");
	var address = $(this).attr("data-address");
	var locality = $(this).attr("data-locality");
	var pincode = $(this).attr("data-pincode");
	var city = $(this).attr("data-city");
	var state = $(this).attr("data-state");

	$("#id_name").val(c_name);
	$("#id_phone").val(phone);
	$("#id_address").val(address);
	$("#id_locality").val(locality);
	$("#id_pincode").val(pincode);
	$("#id_city").val(city);
	$("#id_state").val(state);

	$("form.address_form").attr("action", url);
	$(".add-address").addClass("active");
});

$(".address-pincode").keyup(function (e) {
	var pin = $(this).val();
	var url = $("#pin-checkurl").attr("data-pincheckurl");

	console.log(url);

	if (pin.length < 6) {
		$(".pin_is_available").css({
			display: "none",
		});
	}

	if (pin.length == 6) {
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				pincode: pin,
			},

			success: function (data) {
				console.log(data["status"]);
				if (data["status"] == "available") {
					$(".pin_is_available").css({
						display: "block",
						color: "green",
					});
					$(".pin_is_available").html("Available");
				}

				if (data["status"] == "not_available") {
					$(".pin_is_available").css({
						display: "block",
						color: "red",
					});
					$(".pin_is_available").html(
						"Delivery not available on this area"
					);
				}
			},

			error: function (data) {
				if (data["status"] == "error") {
					var title = "An error occurred";
					var message = "An error occurred. Please try again later.";

					$("#profile-sweet-message").html(message);
					$(".tick-box #title").html(title);

					$("section.all-order").addClass("active");
					$("section.success").addClass("active");
					$("section.number-update").removeClass("active");
				}
			},
		});
	}
});

$("#cart_address_btn").click(function (e) {
	console.log("kereeettundttoooooo");
	$("cart_address_warning").css({
		display: "none",
	});

	address = $(this).attr("data-address_pk");

	if (address !== "") {
		// console.log("haiiiiiiii");

		$("cart_address_warning").css({
			display: "none",
		});

		url = $(this).attr("data-url");
		address = $(this).attr("data-address_pk");

		default_address_save(url, address);
	} else {
		var title = "An error occurred";
		var message = "An error occurred. Please try again later.";

		$("#profile-sweet-message").html(message);
		$(".tick-box #title").html(title);

		$("section.all-order").addClass("active");
		$("section.success").addClass("active");
		$("section.number-update").removeClass("active");
		// console.log("else il kereeekk tto");
		$("#cart_address_warning").css({
			display: "block",
		});
	}
});

function default_address_save(url, address) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			address: address,
		},

		success: function (data) {
			console.log(data["status"]);
			if (data["status"] == "true") {
				var redirect_url = data["redirect_url"];
				location.href = redirect_url;
			}
		},

		error: function (data) {
			if (data["status"] == "error") {
				var title = "An error occurred";
				var message = "An error occurred. Please try again later.";

				$("#profile-sweet-message").html(message);
				$(".tick-box #title").html(title);

				$("section.all-order").addClass("active");
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}
		},
	});
}

function payment_type(id) {
	// console.log(id)

	if (id == "payment_by_card") {
		// console.log("card");
		data = id;
		$("#payment_button").attr("data-payment_type", data);
	}

	if (id == "payment_by_upi") {
		// console.log("upi");
		data = "payment_by_upi";
		$("#payment_button").attr("data-payment_type", data);
	}

	if (id == "payment_by_cod") {
		// console.log("cod");
		data = "payment_by_cod";
		$("#payment_button").attr("data-payment_type", data);
	}
}

$("#payment_button").click(function (e) {
	type = $(this).attr("data-payment_type");
	url = $(this).attr("data-url");

	// order_submit_ajax(type, url);

	if (type == "") {
		var title = "Please Select Payment Type.";
		var message = "Select Payment Type.";

		$("#profile-sweet-message").html(message);
		$(".tick-box #title").html(title);

		$("section.all-order").addClass("active");
		$("section.success").addClass("active");
		$("section.number-update").removeClass("active");
	} else {
		order_submit_ajax(type, url);
	}
});

function order_submit_ajax(type, url) {
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			payment_type: type,
		},

		success: function (data) {
			console.log(data["status"]);
			// if (type == "payment_by_cod") {
			// 	if (data["status"] == "true") {
			// 		var title = "Successfull";
			// 		var message = "product order conformed";

			// 		$("#profile-sweet-message").html(message);
			// 		$(".tick-box #title").html(title);

			// 		$("section.all-order").addClass("active");
			// 		$("section.success").addClass("active");
			// 		$("section.number-update").removeClass("active");
			// 	}
			// }
			var redirect_url = data["redirect_url"];
			location.href = redirect_url;
		},

		error: function (data) {
			if (data["status"] == "error") {
				var title = "An error occurred";
				var message = "An error occurred. Please try again later.";

				$("#profile-sweet-message").html(message);
				$(".tick-box #title").html(title);

				$("section.all-order").addClass("active");
				$("section.success").addClass("active");
				$("section.number-update").removeClass("active");
			}
		},
	});
}

$("#filter_id").on("change", function () {
	$("#sort_form").submit();
	console.log(this.value);
});

// rating-popup
function review_span(order_pk) {
	$(".modal-pop").toggleClass("is-visible");
	pro_pk = $("." + order_pk + "modal-toggle").attr("data-pro_pk");
	$("#id_pro_pk").val(pro_pk);

	let parant = $("." + order_pk + "modal-toggle").parents("li");

	pro_name = parant.find("#pro_name_oder").html();
	image = parant.find("img").attr("src");

	$("#rating_modal_name").html(pro_name);
	$("#rating_modal_img").attr("src", image);

	console.log(pro_pk + "prooooooooooo pk");
}

// size chart from product single view

$(document).ready(function () {
	value = $(".sizeChart_table").attr("data-pro_type");
	console.log(value);

	if (value == "shirt") {
		console.log("shirt");
		$(".brandsize").css({ display: "" });
		$(".size").css({ display: "" });
		$(".chest").css({ display: "" });
		$(".front_length").css({ display: "" });
		$(".accross_sholder").css({ display: "" });
		$(".waist").css({ display: "" });
		$(".sleeve_length").css({ display: "" });
		$(".outseam").css({ display: "none" });
		$(".inseam").css({ display: "none" });
		$(".bottom_hem").css({ display: "none" });
		$(".rise").css({ display: "none" });
		$(".thigh").css({ display: "none" });
	}
	if (value == "pant") {
		console.log("pant");

		$(".brandsize").css({ display: "" });
		$(".size").css({ display: "" });
		$(".waist").css({ display: "" });
		$(".outseam").css({ display: "" });
		$(".inseam").css({ display: "" });
		$(".bottom_hem").css({ display: "" });
		$(".rise").css({ display: "" });
		$(".thigh").css({ display: "" });
		$(".chest").css({ display: "none" });
		$(".front_length").css({ display: "none" });
		$(".sleeve_length").css({ display: "none" });
		$(".accross_sholder").css({ display: "none" });
	}
	if (value == "boxer") {
		console.log("boxer");

		$(".brandsize").css({ display: "" });
		$(".size").css({ display: "" });
		$(".waist").css({ display: "" });
		$(".outseam").css({ display: "" });
		$(".inseam").css({ display: "" });
		$(".rise").css({ display: "" });
		$(".thigh").css({ display: "" });
		$(".chest").css({ display: "none" });
		$(".bottom_hem").css({ display: "none" });
		$(".front_length").css({ display: "none" });
		$(".sleeve_length").css({ display: "none" });
		$(".accross_sholder").css({ display: "none" });
	}
	if (value == "t_shirt") {
		console.log("t_shirt");

		$(".brandsize").css({ display: "" });
		$(".size").css({ display: "" });
		$(".chest").css({ display: "" });
		$(".waist").css({ display: "" });
		$(".accross_sholder").css({ display: "" });
		$(".sleeve_length").css({ display: "" });
		$(".front_length").css({ display: "" });
		$(".outseam").css({ display: "none" });
		$(".inseam").css({ display: "none" });
		$(".rise").css({ display: "none" });
		$(".thigh").css({ display: "none" });
		$(".bottom_hem").css({ display: "none" });
	}
});

// rating
$(".star-rating").click(function (e) {
	var rating = $(".star-rating s.rated").length;
	$("#id_rating").val(rating);
	console.log(rating);
});


function selectedvarient(brand_size_pk) {
	var brand_pk = brand_size_pk
	// console.log(brand_pk,"---");
	url = $("#varient"+brand_pk).attr("data-url");

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		data: {
			brand_pk: brand_pk,
		},

		success: function (data) {
			// console.log(data["status"]);
			if (data["status"] == "true") {
				// console.log("true");
				$("#gotocart_button").css({ display: "block" });
				$("#addtocart_button").css({ display: "none" });
			}
			if (data["status"] == "false") {
				// console.log("false");
				$("#gotocart_button").css({ display: "none" });
				$("#addtocart_button").css({ display: "block" });
			}
		},

		error: function (data) {
			if (data["status"] == "error") {

			}
		},
	});
};