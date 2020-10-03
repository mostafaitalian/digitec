
export const ADD_LOGGEDIN_USER = 'ADD_LOGGEDIN_USER'
export const GET_LOGGEDIN_USER = 'GET_LOGGEDIN_USER'
export const DELETE_LOGGEDIN_USER = 'DELETE_LOGGEDIN_USER'


export function getLoggedInUser(){
    return{
        type:GET_LOGGEDIN_USER,
    }
}

export function addLoggedInUser(user){
    return{
        type:ADD_LOGGEDIN_USER,
        user,
    }
}


export function deleteLoggedInUser(){
    return{
        type:DELETE_LOGGEDIN_USER,
    }
}