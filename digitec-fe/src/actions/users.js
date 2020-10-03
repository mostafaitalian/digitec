


export const ADD_USER= 'ADD_USER'
export const ADD_USERS = 'ADD_USERS'
export const GET_USERS = 'GET_USERS'
export const GET_USER = 'GET_USER'

export function add_User(user){
    return{
        type:ADD_USER,
        user,
    }
}
export function getUsers(){
    return{
        type:GET_USERS
    }
}

export function getUser(id){
    return {
        type:GET_USERS,
        id,
    }
}