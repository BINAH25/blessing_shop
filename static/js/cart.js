let btns = document.getElementsByClassName("addtocart")
for(let i = 0; i < btns.length; i++){
    btns[i].addEventListener('click', function(e){
        let product_id = e.target.dataset.product
        let action = e.target.dataset.action
        if(user=='AnonymousUser'){
            console.log('not log in')
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
})
.catch((error) => {
console.error('Error:', error);
});

}


