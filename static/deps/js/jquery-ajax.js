document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        let button = event.target.closest(".add-to-cart");
        if (!button) return;

        event.preventDefault();
        button.disabled = true; 

        let form = button.closest("form");
        let formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server response:", data);

            if (data.success) {
                let cartCounter = document.querySelector("#goods-in-cart-count");
                if (cartCounter) {
                    cartCounter.textContent = data.total_quantity || 0;
                }

                let cartContainer = document.querySelector("#cart-container");
                if (cartContainer) {
                    cartContainer.innerHTML = data.cart_items_html;
                }

                showSuccessNotification("✅ Product added to cart!");
            } else {
                showErrorNotification(data.message || "❌ Error adding product!");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showErrorNotification("❌ Server error! Try again");
        })
        .finally(() => {
            button.disabled = false;
        });
    });
});


function updateCartCount(newQuantity) {
    let goodsInCartCount = document.getElementById("goods-in-cart-count");
    if (goodsInCartCount) {
        goodsInCartCount.textContent = newQuantity;
    }
}

// Повідомлення
function showSuccessNotification(message) {
    let notification = document.getElementById("jq-notification");

    if (notification) {
        notification.innerHTML = message;
        notification.style.display = "block";
        notification.classList.add("fade-in");

        setTimeout(() => {
            notification.classList.remove("fade-in");
            notification.classList.add("fade-out");

            setTimeout(() => {
                notification.style.display = "none";
                notification.classList.remove("fade-out");
            }, 500);
        }, 4000);
    }
}

$(document).on("click", ".remove-from-cart", function (e) {
    e.preventDefault();

    var cart_id = $(this).data("cart-id");
    var remove_from_cart = $(this).data("remove-url");
    var cartItemElement = $(this).closest(".cart-item");

    console.log("Removing an item from the cart, ID:", cart_id);

    $.ajax({
        type: "POST",
        url: remove_from_cart,
        data: {
            cart_id: cart_id,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
            console.log("The product has been successfully removed:", data.message);

            // Оновлюємо товари в корзині
            var goodsInCartCount = $("#goods-in-cart-count");
            var cartCount = parseInt(goodsInCartCount.text() || 0);
            cartCount -= data.quantity_deleted;
            goodsInCartCount.text(cartCount);

            // Мінус товари
            cartItemElement.fadeOut(300, function () {
                $(this).remove();
            });

            // Оновлюємо кошик
            $("#cart-items-container").html(data.cart_items_html);

            // Показ повідомлення
            showSuccessNotification("🗑️ The product has been removed from the cart!");
        },
        error: function () {
            console.error("Error while deleting item from cart");
            showErrorNotification("❌ Error! Failed to delete item");
        }
    });
});

// Показ повідомлення
function showSuccessNotification(message) {
    let notification = $("#jq-notification");

    if (notification.length === 0) {
        $("body").append('<div id="jq-notification" class="alert alert-success custom-shadow"></div>');
        notification = $("#jq-notification");
    }

    notification.text(message);
    notification.css({
        display: "block",
        opacity: 1
    }).fadeIn(400).delay(3000).fadeOut(400);
}

// Показ помилки
function showErrorNotification(message) {
    let notification = $("#jq-notification");

    if (notification.length === 0) {
        $("body").append('<div id="jq-notification" class="alert alert-danger custom-shadow"></div>');
        notification = $("#jq-notification");
    }

    notification.text(message);
    notification.css({
        display: "block",
        opacity: 1
    }).fadeIn(400).delay(3000).fadeOut(400);
}

    // - мінус товар
    $(document).on("click", ".decrement", function () {

        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        if (currentValue > 1) {
            $input.val(currentValue - 1);

            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // + товар
    $(document).on("click", ".increment", function () {

        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // смс 7 сек 
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Error adding product to cart");
            },
        });
    }

    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();

        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });



