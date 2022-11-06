let btns = document.getElementsByClassName("addtocart")
let cart = document.getElementById('cart')
let cart_items = document.getElementById('cart_items')
let total = document.getElementById('total')
for(let i = 0; i < btns.length; i++){
    btns[i].addEventListener('click', function(e){
        let product_id = e.target.dataset.product
        let action = e.target.dataset.action
        if(user=='AnonymousUser'){
            alert('you need to login first')
        }
        else{
            addToCart(product_id,action)
            console.log(user)
        }
    })
}

function addToCart(p_id, act){
  const data = {product_id: p_id, action: act};
let url = '/update_cart'
fetch(url, {
method: 'POST', // or 'PUT'
headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
},
body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => {
console.log('Success:', data);
cart.innerText = data.quantity
})
.catch((error) => {
console.error('Error:', error);
});

}

let inputfields = document.getElementsByTagName('input')
for(let i =0; i<inputfields.length; i++){
  inputfields[i].addEventListener('change', updateQuantity)
  
}

function updateQuantity(e){
  let inputvalue = e.target.value
if (inputvalue < 2) {
  inputvalue = 1    
}
let product_id = e.target.dataset.product
let p
const data = {p_id: product_id, in_val: inputvalue};
let url = '/update_quantity'

fetch(url, {
method: 'POST', // or 'PUT'
headers: {
  'Content-Type': 'application/json',
  'X-CSRFToken': csrftoken
},
body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => {
  console.log('Success:', data);
  e.target.parentElement.parentElement.children[2].innerHTML = `<strong id="subtotal">SubTotal: GH$${data.subtotal.toFixed(2)}</strong>`
  cart_items.innerHTML = `<strong id="cart_items">${data.quantity}</strong>`
  total.innerHTML = `<strong id="cart_items">GH$${data.total.toFixed(2)}</strong>`
})
.catch((error) => {
  console.error('Error:', error);
});

}

