


function addShop(goods_id) {
    // 这里必须传入商品得id,说明是那个商品在购物车里得数据增加一
    csrf = $('input[name="csrfmiddlewaretoken"]').val()  // 这里是解决csrf验证得问题
    $.ajax({
        url: '/goods/addgoods/', // 通过那个函数方法来实现想要得方法
        type:'POST',  // 请求类型
        headers:{'X-CSRFToken': csrf}, // 解决csrf验证得问题
        data: {'goods_id':goods_id},  //这里是将页面传入的参数，返回到函数方法中。
        dataType: 'json',
        success: function(msg){
            $('#num_' + goods_id).html(msg.c_num)  // 在页面里渲染出数据库里的数据，这里的msg是函数返回到页面的json数据，这里相当与进行了两次交互。
            // 第一次是将页面的数据传入函数，第二次是将函数返回的数据，渲染到页面。
        },
        error:function(){
            alert('请求错误！')
        }
    });
}


function subShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/goods/subgoods/',
        type:'POST',
        data: {'goods_id':goods_id},
        headers:{'X-CSRFToken': csrf},
        dataType: 'json',
        success: function(msg){
            $('#num_' + goods_id).html(msg.c_num)
        },
        error:function(){
             alert('请求错误！')
        }
    });
}

function changeselect(id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/goods/changeCartSelect/',
        type: 'POST',
        data: {'id':id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function(msg){
            if (msg.is_select){
                s = '<span onclick="changeselect(' +  id + ')">√</span>'
            }else{
                s= '<span onclick="changeselect(' + id + ')">x</span>'
            }
            $('#changeselect_' + id).html(s)
            $('#count_price').html('总价：' + msg.count_price)
        },
        error:function(){
            alert('请求错误！')
        }
    })
}

function carts_select_all() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/goods/cartsSelectAll/',
        type: 'GET',
        // data: {'carts':carts},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function(msg){
            window.location.reload()
        },
        error:function(msg){
            alert('请求错误！')
        }
    })
}