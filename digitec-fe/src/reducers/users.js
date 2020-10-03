import {ADD_USER, ADD_USERS, GET_USER, GET_USERS} from '../actions/users'


export default function users(state={}, action){
    switch (action.type) {
        case ADD_USER:
            return {...state,...action.user}
        case ADD_USERS:
            return {...state, ...action.users}
        case GET_USERS:
            return {...state}
        case GET_USER:
            return state
        default:
            return state;
    }
}