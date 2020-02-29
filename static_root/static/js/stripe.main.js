$(document).ready(function () {
  var stripeFormModule = $(".stripe-payment-form")
  var stripeModuleToken = stripeFormModule.attr('data-token')
  var stripeModuleNextUrl = stripeFormModule.attr('data-next-url')
  var stripeModuleBtnTitle = stripeFormModule.attr('data-btn-title') || "Add Card"
  var stripeTemplate = $.templates('#stripeTemplate')
  var stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    btnTitle: stripeModuleBtnTitle
  }
  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
  stripeFormModule.html(stripeTemplateHtml)



  var paymentForm = $('.payment-form')
  if (paymentForm.length > 1) {
    console.log('Only one payment method form allowed.')
    paymentForm.css('display', 'none')
  }

  else if (paymentForm.length == 1) {

    var pubKey = paymentForm.attr('data-token')
    var nextUrl = paymentForm.attr('data-next-url')

    // Create a Stripe client.
    var stripe = Stripe(pubKey);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', { style: style });

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function (event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });

    // // Handle form submission.
    // var form = document.getElementById('payment-form');
    // form.addEventListener('submit', function (event) {
    //   event.preventDefault();

    //   stripe.createToken(card).then(function (result) {
    //     if (result.error) {
    //       // Inform the user if there was an error.
    //       var errorElement = document.getElementById('card-errors');
    //       errorElement.textContent = result.error.message;
          
    //     } else {
    //       // Send the token to your server.
    //       stripeTokenHandler(nextUrl, result.token);
          
    //     }
    //   });
    // });

    // Handle form submission.
    var form = $('.payment-form');
    form.on('submit', function (event) {
      event.preventDefault();

      var btn = $(this).find(".btn-load")
      var errorHtml = "<i class='fa fa-warning'></i> An error occured"
      var loadHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
      var errorClasses = "btn btn-warning disabled my-3"
      var loadClasses = "btn btn-success disabled my-3"

      stripe.createToken(card).then(function (result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;

          displayBtn(btn, errorHtml, errorClasses)
          
          
        } else {
          // Send the token to your server.
          stripeTokenHandler(nextUrl, result.token);
          
          displayBtn(btn, loadHtml, loadClasses)
        }
      });
    });


    function displayBtn(element, newHtml, newClasses){
      var defaultHtml = element.html()
      var defaultClasses = element.attr('class')

      element.html(newHtml)
      element.removeClass(defaultClasses)
      element.addClass(newClasses)
      setTimeout(function(){
        element.html(defaultHtml)
        element.removeClass(newClasses)
        element.addClass(defaultClasses)
      }, 1000)
    }





    function redirectToNext(nextPath, timeOffset) {
      if (nextPath) {
        setTimeout(function () {
          window.location.href = nextUrl
        }, timeOffset)
      }
    }

    // Submit the form with the token ID.
    function stripeTokenHandler(nextUrl, token) {
      var paymentMethodEndPoint = '/billings/payment-method/create/'
      var data = {
        'token': token.id
      }
      $.ajax({
        data: data,
        url: paymentMethodEndPoint,
        method: 'POST',
        success: function (data) {
          var successMsg = "Success! your card was added." || data.message
          card.clear();
          if (nextUrl) {
            successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
          }
          if ($.alert) {
            $.alert(successMsg)
            redirectToNext(nextUrl, 1500)
          } else {
            alert(successMsg)
          }
          redirectToNext(nextUrl, 1500)
        },

        error: function (error) {
          $.alert({title: 'An error occured', content: "Please try to add your card!"})
        }

      });
    }

  }


})
