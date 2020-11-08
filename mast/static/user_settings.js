function display_update_profile() {
    let update_element = document.getElementById('update_profile_div')
    let change_password_element = document.getElementById('change_password_div')
    if (change_password_element.style.display != 'none') {
        change_password_element.style.display = 'none'
    }
    update_element.style.display = 'block'
}

function display_change_password() {
    let update_element = document.getElementById('update_profile_div')
    let change_password_element = document.getElementById('change_password_div')
    if (update_element.style.display != 'none') {
        update_element.style.display = 'none'
    }
    change_password_element.style.display = 'block'
}