//#region ------------------------------ 全域變數 ------------------------------
// 存放菜單的陣列(sort by catId)
let menuList = [];
// let theProducts = []; //存放菜單的陣列(sort by productId)
let theUserOrders = []; //客人的歷史訂單
// let theFoodAdditions = []; //食物附加選項
const expireMins = 30; //登入過期時間(分鐘)
// const urlDomain = 'http://localhost:3000';
const urlDomain = 'https://json-server-vercel-a.vercel.app';

//#endregion

$(function () {

    init();
    //監聽分類標籤
    $('input[name="cat-tags"]').on('change', catTagsChangeHandler);
    $("#logo").on("click", function () {
        $("#cat-tag-all").click();
        $('#menu').animate({ scrollTop: 0 }, 'fast');
    })
    $("#productModal").on("change", "#foodAdditionOptions input.foodAdditionOption", function () {
        btnAdditionChange();
    });

    // 點選商品項目
    $("#menu").on("click", ".food-card", foodCardClickHandler);
    // 按下加入購物車按鈕
    $(".add-to-cart-btn").on('click', addToCartBtnClickHandler);
    // 按下查看購物車按鈕
    $(".show-cart-btn").on('click', showCartBtnClickHandler);
    $(".switch-user-page").on('click', switchUserPageClickHandler);

    // var token = "";
    // axios.post(`http://127.0.0.1:8000/api/token/`, {
    //     username: "admin",
    //     password: 'cl3ru4au4a83',
    // }).then(function (response) {
    //     token = response.data.access;
    //     const config = {
    //         headers: {
    //             'Authorization': `Bearer ${token}`,
    //             'Content-Type': 'application/json'
    //         }
    //     }
    //     axios.post(`http://127.0.0.1:8000/api/products/`, {
    //         name: "蛋餅",
    //         price: 100,
    //         stock: 10
    //     },config)
    //         .then(function (response) {
    //             console.log(response);
    //         }).catch(function (error) {
    //             console.log('error', error);
    //         });
    // }).catch(function (error) {
    //     console.log('error', error);
    // });
})

//#region ------------------------------ DOM EVENT處理 ------------------------------

/**
 * 切換分類標籤事件
 *
 * @param {Event} e - 變更事件對象
 * @returns {void}
 */
function catTagsChangeHandler(e) {
    // 目前的分類ID
    const catId = parseInt($("input[name='cat-tags']:checked").val());
    if (catId < 0) {
        // 顯示全部
        $('div[name="cat-area"]').show();
    } else {
        // 顯示特定
        $('div[name="cat-area"]').hide();
        $(`div[name="cat-area"][data-cat-id="${catId}"]`).show();
    }
}

/**
 * 按下商品事件
 *
 * @param {Event} e - 變更事件對象
 * @returns {void}
 */
function foodCardClickHandler(e) {
    let $modal = $('#productModal');
    // 商品ID
    let productId = parseInt($(this).attr("data-product-id"));
    // 將資訊放入modal中
    renderProductModal(productId);
    $modal.attr("data-product-id", productId);
    // 開啟商品視窗
    $modal.modal('show');
}

/**
 * 按下"加入購物車"按鈕事件
 *
 * @param {Event} e - 觸發事件對象
 * @returns {void}
 */
function addToCartBtnClickHandler(e) {
    // 分類ID
    const catId = parseInt($(this).attr('data-cat-id'));
    // 商品ID
    const productId = parseInt($(this).attr('data-product-id'));
    // 加入購物車
    addToCart(catId, productId);
}

/**
 * 按下"查看購物車"按鈕事件
 *
 * @param {Event} e - 觸發事件對象
 * @returns {void}
 */
function showCartBtnClickHandler(e) {
    let $modal = $('#cartModal');
    // 更新顯示購物車內容modal
    renderCartModal();
    $modal.modal('show');
}

/**
 * 切換會員相關功能頁
 *
 * @param {Event} e  - 觸發事件對象
 * @returns {void}
 */
function switchUserPageClickHandler(e){
    const toPage = $(this).attr("data-topage");
    $(".user-modal-body-page").hide();
    renderUserModal(toPage);
}

//#region ------------------------------ 邏輯流程 ------------------------------
//初始化
function init() {
    //檢查網址參數
    const urlParams = new URLSearchParams(window.location.search);
    const isInsider = urlParams.has('insider');
    if (isInsider) {
        login('A3@store.com', 'abc123');
        return;
    }
    //檢查登入狀態
    if (getDataFromLocalStorage('_user')) {
        chkTimer();
    }
    // getMenu();
    renderNavList();
    renderQrCode();
    updateFooterTotalPrice();
}

/**
 * 移動到後台
 *
 * @returns {void}
 */
function goToBackstage() {
    window.location.href = 'backstage.html';
}

//彈出歷史訂單Modal
function showUserOrderModal() {
    getUserOrders();
}

//彈出loginModal
function showLoginModal() {
    renderUserModal("login");
    $('#user-modal').modal('show');
}
//彈出廣告Modal
function showAdModal() {
    $('#adModal').modal('show');
}
//彈出導覽Modal
function showGuideModal() {
    $('#guideModal').modal('show');
}

/**
 * 將商品加入購物車
 *
 * @param {interger} catId - 分類ID
 * @param {interger} productId - 商品ID
 * @returns {void}
 */
function addToCart(catId, productId) {
    const productName = $(".product-modal-name").text();
    const carts = getCarts();
    const qty = parseInt($('#tempProductAmount').text());
    const comment = $('#tempProductComment').val();

    let additems = [];
    $('#foodAdditionOptions input.foodAdditionOption:checked').each(function () {
        additems.push($(this).val());
    });
    const price = parseInt($("#tempProductTotal").text());
    carts.push({
        catId: catId,
        id: productId,
        name: productName,
        price: price / qty,
        qty: qty,
        comment: comment,
        additems: additems,
    });
    saveDataToLocalStorage('cart', carts);
    $('#productModal').modal('hide');
    updateFooterTotalPrice();
}

/**
 * 更新購物車內容
 *
 * @param {interger} productIndex - 商品索引
 * @returns {void}
 */
function updateToCart(productIndex) {
    const carts = getCarts();
    const qty = parseInt($('#tempProductAmount').text());
    const comment = $('#tempProductComment').val();
    const additems = [];
    $('#foodAdditionOptions input.foodAdditionOption:checked').each(function () {
        additems.push($(this).val());
    });
    const price = parseInt($("#tempProductTotal").text());
    carts[productIndex].qty = qty;
    carts[productIndex].comment = comment;
    carts[productIndex].additems = additems;
    carts[productIndex].price = price / qty;
    saveDataToLocalStorage('cart', carts);
    sweetSmallSuccess('已更新購物車');
    $('#productModal').modal('hide');
    showCartModal();
    updateFooterTotalPrice();
}


//送出購物車訂單
function submitCart() {
    const carts = getCarts();
    if (carts.length == 0) {
        sweetError('購物車沒有商品', '請先加入商品');
        return;
    } else if (getDataFromLocalStorage('_token') == null) {
        saveDataToLocalStorage('returnModal', 'cartModal');
        $("#cartModal").modal('hide');
        showLoginModal()
        return;
    }
    const order = {
        id: "OD" + (+new Date()).toString(),
        userId: getDataFromLocalStorage('_user').id,
        name: getDataFromLocalStorage('_user').name,
        phone: getDataFromLocalStorage('_user').phone,
        comment: $('#cartComment').val(),
        price: countCartTotalPrice(),
        orderDate: getTimeNow().split(" ")[0],
        orderTime: getTimeNow().split(" ")[1],
        takeWay: $('#cartTakeWay input:checked').val(),
        isPaid: false,
        isDone: false,
        details: carts,
    }
    postCartOrder(order);
}
//更新footer的訂單小計
function updateFooterTotalPrice() {
    $("#footerTotalPrice").text(countCartTotalPrice());
}
//讀取購物車內容
function getCarts() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    return cart;
}
//調整商品數量
function adjAmount(price, method) {
    let tempProductAmount = parseInt($('#tempProductAmount').text());
    if (method == 'add') {
        tempProductAmount++;
    } else if (method == 'minus' && tempProductAmount > 1) {
        tempProductAmount--;
    }
    $('#tempProductAmount').text(tempProductAmount);
    countCurrentPrice();
    //$('#tempProductTotal').text(`${price * tempProductAmount}`);
}
//附加選項增減
function btnAdditionChange() {
    let addPrice = 0;
    $("#foodAdditionOptions input.foodAdditionOption:checked").each(function () {
        addPrice += parseInt($(this).attr('data-add-price'));
    })
    $('#tempProductTotal').attr('data-add-price', addPrice);
    countCurrentPrice();
}

//計算產品總價
function countCurrentPrice() {
    const foodPrice = parseInt($('#tempProductTotal').attr('data-food-price'));
    const additionPrice = parseInt($('#tempProductTotal').attr('data-add-price'));
    const qty = parseInt($('#tempProductAmount').text());
    const currentPrice = (foodPrice + additionPrice) * qty;
    $('#tempProductTotal').text(currentPrice);
}
//計算購物車總金額
function countCartTotalPrice() {
    let cartList = getCarts();
    let totalPrice = 0;
    cartList.forEach(productObj => {
        totalPrice += productObj.price * productObj.qty;
    })
    return totalPrice;
}
//刪除購物車商品
function deleteCartProduct(productIndex) {
    let cartList = getCarts();
    cartList.splice(productIndex, 1);
    saveDataToLocalStorage('cart', cartList);
    renderCartModal();
    updateFooterTotalPrice();
}
//編輯購物車商品
function editCartProduct(productId, productIndex) {
    $('#cartModal').modal('hide');
    renderProductModal(productId);
    let cartList = getCarts();
    let productObj = cartList[productIndex];
    $('#tempProductAmount').text(productObj.qty);
    $('#tempProductComment').val(productObj.comment);
    $('#tempProductTotal').text(`${productObj.price * productObj.qty}`);
    $('#btnAddToCart').attr('onclick', `updateToCart(${productIndex})`);
    $('#productModal').modal('show');
    productObj.additems.forEach(additem => {
        $(`#foodAdditionOptions input[value=${additem}]`).prop('checked', true);
    })

}
//demo Input 填入
function demoInput(demoName) {
    switch (demoName) {
        case '小明':
            $('#loginEmail').val('ming@gmail.com');
            $('#loginPassword').val('abc123');
            break;
        case '阿姨':
            $('#loginEmail').val('anti@gmail.com');
            $('#loginPassword').val('iamboss');
            break;
        default:
            $('#loginEmail').val('');
            $('#loginPassword').val('');
            break;
    }
}
//從導覽Modal跳轉到登入Modal
function goToLoginModalWithName(demoName) {
    $('#guideModal').modal('hide');
    showLoginModal();
    demoInput(demoName);
}
//check login info
function btnLogin(callbackModal = "") {
    const email = $("#login-page-username").val();
    const password = $("#login-page-password").val();
    login(email, password)
}
//btnRegister
function btnRegister() {
    const name = $('#register-page-name').val();
    const email = $('#register-page-email').val();
    const phone = $('#register-page-phone').val();
    const password = $('#register-page-password').val();
    if (name == '' || phone == '' || email == '' || password == '') {
        sweetError('請輸入完整資料');
        return;
    }
    let model = {
        password: password,
        name: name,
        email: email,
        phone: phone,
        role: 'customer'
    }
    register(model);
}

//switch modal 關閉現在的modal，開啟前一次的modal
function switchModal() {
    const returnModal = getDataFromLocalStorage('returnModal');
    $(".modal").modal('hide');
    switch (returnModal) {
        case 'cartModal':
            showCartModal();
            break;
        // case 'productModal':
        //     $('#productModal').modal('show');
        //     break;
        case 'orderModal':
            showUserOrderModal();
            break;
    }
    deleteDataFromLocalStorage('returnModal');
}
//附加選項id轉name
function additionIdToName(additionId) {
    let name = Object.values(theFoodAdditions).reduce((a, b) => [...a, ...b.items], []).find(item => item.id == additionId)?.name
    return name ? name : '';
}

//catIdToCatName
function catIdToCatName(catId) {
    let catName = Object.values(menuList).find(item => item.id == catId)?.name;
    return catName ? catName : '';
}
//#endregion


//#region ------------------------------ API ------------------------------

//取得用戶歷史訂單
function getUserOrders() {
    const userId = getDataFromLocalStorage('_user').id;
    const token = getDataFromLocalStorage('_token');
    const config = { headers: { 'Authorization': `Bearer ${token}` } }
    axios.get(`${urlDomain}/600/orders?userId=${userId}`, config)
        .then(function (response) {
            theUserOrders = response.data.reverse();
            console.log('theUserOrders', theUserOrders);
            renderUserOrdersModal();
        }).catch(function (error) {
            console.log('error', error);
            theUserOrders = [];
            renderUserOrdersModal();
        });
}
//login
function login(username, password) {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    }
    axios.post("/api/token/", {
            username: username,
            password: password
        }, config)
        .then(function (response) {
            console.log(response.data);
            // response.data.access

        }).catch(function (error) {
            sweetError('登入失敗', '帳號或密碼錯誤');
        });


    // axios.post(`${urlDomain}/login`, { email: email, password: password })
    //     .then(function (response) {
    //         saveDataToLocalStorage('_token', response.data.accessToken);
    //         saveDataToLocalStorage('_user', response.data.user);
    //         saveDataToLocalStorage('_expire', { time: new Date().getTime(), expire: expireMins * 60 * 1000 });
    //         chkTimer();
    //         if (response.data.user.role == 'admin') {
    //             deleteDataFromLocalStorage('returnModal');
    //             window.location.href = 'backstage.html';
    //             return;
    //         }
    //         if (response.data.user.role == 'insider') {
    //             window.location.href = window.location.origin + window.location.pathname;
    //             return;
    //         }

    //         $('#loginModal').modal('hide');
    //         renderNavList();
    //         switchModal();
    //         if (response.data.user.role == 'insider') {
    //             sweetSmallSuccess(`桌號 ${response.data.user.name}，歡迎光臨`);
    //         } else {
    //             sweetSmallSuccess(`早安😀 ${response.data.user.name}，登入成功`);
    //         }

    //     }).catch(function (error) {
    //         sweetError('登入失敗', '帳號或密碼錯誤');
    //     });

}
//logout
function logout() {
    deleteDataFromLocalStorage('_token');
    deleteDataFromLocalStorage('_user');
    deleteDataFromLocalStorage('_expire');
    deleteDataFromLocalStorage('returnModal');
    renderNavList();
}
//register
function register(model) {
    axios.post(`${urlDomain}/register`, model)
        .then(function (response) {
            saveDataToLocalStorage('_token', response.data.accessToken);
            saveDataToLocalStorage('_user', response.data.user);
            $('#user-modal').modal('hide');
            renderNavList();
            switchModal();
            sweetSmallSuccess('註冊成功');
        }).catch(function (error) {
            console.log('error', error);
        });
}
//post cart order with token
function postCartOrder(order) {
    const token = getDataFromLocalStorage('_token');
    axios.post(`${urlDomain}/600/orders`, order, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }).then(function (response) {
        sweetSuccess('訂單送出成功', '將盡快為您備餐', 2500);
        switchModal();
        deleteDataFromLocalStorage('cart');
        updateFooterTotalPrice();
    }).catch(function (error) {
        sweetError('訂單送出失敗', '請重新嘗試');
        console.log('error', error);
    });
}

//#endregion

//#region ------------------------------ 渲染畫面 ------------------------------

// 渲染商品Modal
function renderProductModal(productId) {
    let $card = $(".menu-card").filter("[data-product-id='" + productId + "']"),
        catId = $card.attr("data-cat-id"),
        name = $card.find(".menu-p-name").html(),
        content = $card.find(".menu-p-content").html(),
        price = $card.find(".menu-p-price").html(),
        img = $card.find(".menu-card-img").attr('src'),
        isSoldOut = false;
    let addiIds = $card.attr("data-addition-ids").toString().trim();
    addiIds = addiIds.split(",").filter(elem => elem);

    // 商品的附加選項
    addiOptHtml = getAddiOptsHtml(addiIds);

    // 商品的資訊
    $(".product-modal-name").html(name);
    $(".product-modal-content").html(content);
    $(".product-modal-price").html(price);
    $(".product-modal-img").attr("src", img);
    $("#foodAdditionOptions").html(addiOptHtml);
    $(".product-modal-temp-total").attr("data-food-price", price)
                                  .attr("data-total-price", price)
                                  .html(price);
    // 加入購物車按鈕
    $(".add-to-cart-btn").attr("data-cat-id", catId);
    $(".add-to-cart-btn").attr("data-product-id", productId);
}


//渲染購物車Modal
function renderCartModal() {
    let cartList = getCarts();
    // 購物車內容
    let cartCont = "";
    if (cartList.length == 0){
        cartCont += "<div class='text-center'>購物車內沒有商品</div>";
    }else{
        cartList.map((obj, index) => {
            cartCont += getCartItemsHtml(obj, index);
        });
    }
    $("#cart-modal-product-details").html(cartCont);
    $("#tempCartTotalPrice").html(`($${countCartTotalPrice()})`);
}
//渲染歷史訂單Modal //todo
function renderUserOrdersModal() {
    let contents = [];
    if (theUserOrders.length > 0) {
        theUserOrders.forEach(orderObj => {
            let { id, userId, name, phone, comment, price, orderDate, orderTime, isPaid, isDone, details } = orderObj;
            let detailContent = details.map(foodObj => {
                let str = `
            <div class="cartfoodCard d-block mb-2" data-id="${foodObj.id}" data-price="${foodObj.price}">
                <span class="h6 fw-bolder text-start">${foodObj.name}</span>
                <br/>
                <span class="fw-light">${foodObj.comment ? (foodObj.comment + " / ") : ''}</span>
                <span class="fw-light">${foodObj.additems.length > 0 ? foodObj.additems.map(x => additionIdToName(x)).join("/") : ''}</span>
                <div class="d-flex justify-content-between">
                    <span class="fw-light">${foodObj.qty}份</span>
                    <div class="text-danger fw-bold">$${foodObj.price * foodObj.qty}</div>
                </div>
            </div>`
                return str;
            })
            let content = `
        <div
            class="cartfoodCard d-flex mb-2"
            data-order-id="${id}"
            data-bs-toggle="collapse"
            data-bs-target="#collapseOrder-${id}"
        >
            <div>
                <div class="">
                    <span class="h6 fw-bolder">訂單日期</span>
                    <span class="fw-light">${orderDate} ${orderTime}</span>
                </div>
                <div>
                    <span class="h6 fw-bolder">訂單編號</span>
                    <span class="fw-light">${id}</span>
                </div>
            </div>
            <div class="d-flex flex-column ms-auto">
                <span>${isDone ? '已完成' : '製作中'}</span>
                <span class="text-danger fw-bold ms-auto">$${price}</span>
            </div>
        </div>
        <div class="collapse px-3 pt-0 pb-3" id="collapseOrder-${id}">
            ${detailContent.join("")}
        </div>`
            contents.push(content);
        })
    } else {
        contents.push(`<div class="text-center">沒有訂單</div>`)
    }
    $("#userOrdersModal .modal-body").html(contents.join(""));
    $('#userOrdersModal').modal('show');
}
//渲染NAV清單
function renderNavList() {
    let isLogin = getDataFromLocalStorage('_token') ? true : false;
    let isAdmin = getDataFromLocalStorage('_user') ? getDataFromLocalStorage('_user').role == 'admin' : false;
    let userNameContent = "";
    let loginoutContent = `<span class="nav-link finger" href="" onclick="showLoginModal('login')">登入/註冊</span>`;
    if (isLogin) {
        let helloStr = getDataFromLocalStorage('_user').role == 'insider' ? '桌號 ' : '早安!';
        userNameContent = `
        <li class="nav-item" id="navLoginArea">
            <span class="nav-link" href="" id="">${helloStr}  <b>${getDataFromLocalStorage('_user').name}</b></span>
        </li>
        ` ;
        loginoutContent = `<span class="nav-link finger" href="" onclick=
        "logout()">登出</span>`
    }

    let content = `
    ${userNameContent}
    <li class="nav-item">
        <span class="nav-link finger" onclick="showAdModal()">活動快訊</span>
    </li>
    <li class="nav-item">
        <span class="nav-link finger" onclick="showGuideModal()">功能介紹</span>
    </li>
    <li class="nav-item">
        ${isLogin ? '<span class="nav-link finger" onclick="showUserOrderModal()">訂單查詢</span>' : ''}
    </li>
    <li class="nav-item">
        ${isAdmin ? '<span class="nav-link finger" onclick="goToBackstage()">切換至後台</span>' : ''}
    </li>
    <li class="nav-item" id="">
        ${loginoutContent}
    </li>
    `;
    $("#navList").html(content);
}
//渲染User Modal
function renderUserModal(uPage = 'login') {
    $(".user-modal-body-page").hide();
    if (uPage == 'login') {
        $(".user-login-page").show();
    } else if (uPage == 'register'){
        $(".user-register-page").show();
    }
}
//渲染qr code
function renderQrCode() {

    // let str = "https://coldingpotato.github.io/onlineOrder/" + "?insider=A3"

    //let str = window.location.origin + window.location.pathname + "?insider=A3"
    let str = "https://coldingpotato.github.io/onlineOrder/redirect.html?insider=A3"
    $("#qrCode").qrcode({ width: 135, height: 135, text: str });
    $("#qrCode").attr('onclick', `window.open('${str}', '_self')`)
}

//#endregion

//#region ------------------------------ 其他 ------------------------------

//sweetAlert 右上角 小成功
function sweetSmallSuccess(title, timer = 1500) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: timer,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'success',
        title: title
    })
}
//sweetAlert 成功
function sweetSuccess(title, text, timer = 1500) {
    Swal.fire({
        icon: 'success',
        title: title,
        text: text,
        showConfirmButton: false,
        timer: timer
    })
}
//sweetAlert 失敗
function sweetError(title, text) {
    Swal.fire({
        icon: 'error',
        title: title,
        text: text,
        showConfirmButton: false,
        timer: 1500
    })
}
//sweetAlert 資訊
function sweetInfo(title, timer = 3000) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: timer,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'info',
        title: title
    })
}
//檢查localStorage是否過期
function chkTimer() {
    var timer = setInterval(function () {
        if (localStorage.getItem('_expire')) {
            let expireTime = getDataFromLocalStorage('_expire');
            if (new Date().getTime() - expireTime.time > expireTime.expire) {
                sweetInfo('登入逾時，請重新登入', 3000);
                logout()
                clearInterval(timer);
            }
        } else {
            console.log('帳號已登出，localStorage已失效');
            clearInterval(timer);
        }
    }, 1000);
}

//#region ------------------------------ 回傳HTML內容 ------------------------------

/**
 * 回傳顯示追加項目的HTML CODE
 *
 * @param {Array} addiIds  追加項目ID陣列
 * @returns {String} html字串
 */
function getAddiOptsHtml(addiIds) {
    let addiOpts = [];
    if (addiIds.length > 0){
        addiOpts = addiIds.map(addiId => {
            let addiObj = cat_add_list.find(x => x.id == addiId);
            let str = `<div class="" data-addtion-id="${addiObj.id}">
                            <label>${addiObj.name}</label>
                            <hr class="my-1"/>

                            ${addiObj.additions.map(addiItem => {
                return `<input type="${addiObj.is_multiple ? 'checkbox' : 'radio'}" class="btn-check foodAdditionOption" name="${addiObj.name}" id="add-${addiItem.id}" value="${addiItem.id}" data-add-price="${addiItem.price}">
                                        <label class="btn btn-pill-primary" for="add-${addiItem.id}" >${addiItem.name} +$${addiItem.price}</label>`;
            }).join('')}
                        </div>`;
            return str;
        });
    }
    return addiOpts.join('');
}

/**
 * 回傳購物車項目中的HTML CODE
 *
 * @param {Object} obj  商品資訊
 * @param {Interger} index  商品索引
 * @returns {String} html字串
 */
function getCartItemsHtml(obj, index){
    const { id, name, price, qty, comment, additems } = obj;
    return `
    <div class="cartfoodCard d-block mb-2" data-id="${id}" data-price="${price}">
        <div class="d-flex justify-content-between mb-2">
            <span class="h6 fw-bolder">${name}</span>
            <div class="">
                <button class="btn rounded-circle btn-sm cartEdit" onclick="editCartProduct('${id}','${index}')"><i class="fa-solid fa-pencil"></i></button>
                <button class="btn rounded-circle btn-sm cartDelete" onclick="deleteCartProduct('${index}')"><i class="fa-solid fa-trash-can"></i></button>
            </div>
        </div>

        <span class="h6 fw-light d-block">${comment ? (comment) : ""}</span>
        <span class="h6 fw-light d-block">${additems.map(x => additionIdToName(x)).join("/")}</span>
        <div class="d-flex justify-content-between">

            <span class="fw-light">$${price} / ${qty}份</span>
            <div class="text-danger fw-bold">$${price * qty}</div>
        </div>
    </div>`;
}