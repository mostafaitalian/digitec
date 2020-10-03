import {ADD_MACHINE, ADD_MACHINES, GET_MACHINE, DELETE_MACHINE, GET_MACHINES} from '../actions/machines'


export default function machines(state={}, action){
    switch (action.type) {
        case GET_MACHINES:
            return {...state}
        case ADD_MACHINES:
            return {...state,...action.machines}
        case ADD_MACHINE:
            return{...state, ...action.machine}    
    
        default:
            return state;
    }
}