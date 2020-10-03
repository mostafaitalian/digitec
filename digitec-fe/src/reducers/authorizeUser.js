import {ADD_LOGGEDIN_USER, GET_LOGGEDIN_USER, DELETE_LOGGEDIN_USER} from '../actions/authorizeUser'


export default function loggedInUser(state={}, action){
    switch (action.type) {
        case ADD_LOGGEDIN_USER:
            return {...action.user}
            
            break;
        case GET_LOGGEDIN_USER:
            return state
        case DELETE_LOGGEDIN_USER:
            return {}
        default:
            return state;
    }
}
