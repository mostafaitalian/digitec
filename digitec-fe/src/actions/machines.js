



export const ADD_MACHINES = 'ADD_MACHINES'
export const ADD_MACHINE = 'ADD_MACHINE'
export const DELETE_MACHINE = 'DELETE_MACHINE'
export const GET_MACHINE = 'GET_MACHINE'
export const GET_MACHINES = 'GET_MACHINES'

export function addMachine(machine){
    return {
        type:ADD_MACHINE,
        machine,
    }
}

export function addMachines(machines){
    return{
        type:ADD_MACHINES,
        machines,
    }
}

export function deleteMachine(id){
    return{
        type:DELETE_MACHINE,
        id,
    }
}

export function getMachine(id){
    return {
        type:GET_MACHINE,
    }
}

export function getMachines(){
    return{
        type:GET_MACHINES
    }
}