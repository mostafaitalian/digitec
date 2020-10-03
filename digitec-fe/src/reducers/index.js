import {combineReducers} from 'redux'
import machines from './machines'
import users from './users'
import loggedInUser from './authorizeUser'


export default combineReducers({
    loggedInUser,
    machines,
    users,

})