import {combineReducers} from 'redux'
import machines from './machines'
import users from './users'
import loggedInUser from './authorizeUser'
import {loadingBarReducer} from 'react-redux-loading'


export default combineReducers({
    loggedInUser,
    machines,
    users,
    loadingBarReducer,

})