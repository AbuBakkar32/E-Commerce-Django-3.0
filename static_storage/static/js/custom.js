

  
$(function(){
  // register section 
  $('#register-email,#register-password,#register-password2,#register-fullname').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid grey',
    'height': '30px',
    'line-height': '0px',
    'margin': '0'
  })
  
  $('#register-email,#register-password,#register-password2,#register-fullname').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })
  $('#register-email,#register-password,#register-password2,#register-fullname').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid grey'
    })
  })

  // Login section 
  $('#login-email,#login-password').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid grey',
    'height': '30px',
    'line-height': '0px',
    'margin': '0'
  })

  $('#login-email,#login-password').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })
  $('#login-email,#login-password').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid grey'
    })
  })

  setTimeout(function(){
    $('#login-error-messages,.base-messages').css({
      'display': 'none'
    })
  },3000)

// Guest email 
  $('#guest_email').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid grey',
    'height': '30px',
    'line-height': '0px',
    'margin': '0'
  })
  $('#guest_email').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })
  $('#guest_email').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid grey'
    })
  })

  // Address section 
  $('#full_name,#address_line_1,#address_line_2,#mobile_no,#city,#country,#state,#postal_code').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid #e6e6e6',
    'height': '33px',
    'line-height': '0px',
    'margin': '0'
  })
  
  $('#full_name,#address_line_1,#address_line_2,#mobile_no,#city,#country,#state,#postal_code').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })

  $('#full_name,#address_line_1,#address_line_2,#mobile_no,#city,#country,#state,#postal_code').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid #e6e6e6'
    })
  })

  // contact section 
  $('#message').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid #e6e6e6',
  })
  $('#full_name,#email').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid #e6e6e6',
    'height': '33px',
    'line-height': '0px',
    'margin': '0'
  })
  
  $('#full_name,#email,#message').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })

  $('#full_name,#email,#message').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid #e6e6e6'
    })
  })



  // Payment method complete section
  var allPaymentOption = $(".payment-option1,.payment-option2,.payment-option3,.payment-option4")
  var allPaymentHeader = $('.payment-header1,.payment-header2,.payment-header3,.payment-header4')
  allPaymentHeader.css({'margin-left': '0px'})
  allPaymentHeader.find('p').css({'color': 'grey'})

  allPaymentHeader.css({
    'cursor':'pointer',
  })
  // allPaymentOption.hover(function(){
  //   $(this).css({
  //     'border':'2px solid #076FCF'
  //   })
  // },function(){
  //     $(this).css({
  //       'border':''
  //     })
  //   })

  $('.payment-header1').click(function(event){
    $('#payment-content1').toggle(300)
    $('#payment-content2,#payment-content3,#payment-content4').hide()
  })

  $('.payment-header2').click(function(event){
    $('#payment-content2').toggle(300)
    $('#payment-content3,#payment-content1,#payment-content4').hide()
   
  })
  $('.payment-header3').click(function(event){
    $('#payment-content3').toggle(300)
    $('#payment-content2,#payment-content1,#payment-content4').hide()
   
  })
  $('.payment-header4').click(function(event){
    $('#payment-content4').toggle(300)
    $('#payment-content2,#payment-content1,#payment-content3').hide()
   
  })


  // password reset or change 
  $('.password_set_input').css({
    'box-shadow': '0 0 4px white',
    'border': '1px solid grey',
    'height': '30px',
    'line-height': '0px',
    'margin': '0'
  })
  $('.password_set_input').focus(function(){
    $(this).css({
      'box-shadow': '0 0 4px #E4AF2C',
      'border': '1px solid #E4AF2C'
    })
  })

  $('.password_set_input').blur(function(){
    $(this).css({
      'box-shadow': '0 0 4px white',
      'border': '1px solid grey'
    })
  })

// Ajax solution 

// CART Button
  var CartUpdate = $(".cart-update-ajax")
  CartUpdate.submit(function(event){
    var thisForm = $(this)
    var cartUpdateUrl = thisForm.attr('action')
    var cartUpdateMethod = 'GET'
    var formData = thisForm.serialize()
    $.ajax({
      url: cartUpdateUrl,
      method: cartUpdateMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-span")
        if(data.added){
          submitSpan.html("<input type='hidden' name='qty' value='0'> <button type='submit' class='btn btn-warning' style='margin-left:0px;background:#F57C00;'>Remove from cart</button>")
        }
        else{
          submitSpan.html('<button type="submit" class="btn btn-warning" style="background:#F57C00;" >Add To Cart</button>')
        }
        var CartCount = $(".nav-cart-count")
        CartCount.text(data.cartCount)
      },
      error: function(data){
        console.log("error")
      }
    })

    event.preventDefault()
  })

  // update form 
    var cartUpdate = $(".cart-update-ajax")
    cartUpdate.submit(function(event){
      var this_ = $(this)
      var cartUpdateUrl = this_.attr('action')
      var cartUpdateMethod = "GET"
      var cartUpdateData = this_.serialize()
      $.ajax({
        url: cartUpdateUrl,
        method: cartUpdateMethod,
        data: cartUpdateData,
        success: function(data){
          console.log("updated")
        },
        error: function(data){
          console.log('Error')
        }
      })
      event.preventDefault()

    })
  
// settings 
	// BS tabs hover (instead - hover write - click)
	$('.tab-menu a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
  })


})












// lightbox 
lightbox.option({
    'resizeDuration': 200,
    'wrapAround': true,
    "alwaysShowNavOnTouchDevices":true
  });





