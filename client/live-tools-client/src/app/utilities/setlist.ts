import { IAction } from "../services/web-socket/web-socket.service";


export function getSongNbr(action_nbr: number, actions: IAction[]) {
    let counter = 0;
    let nbr = 0;
    actions.forEach(action => {
        if (action.type === "song") counter ++
        if (action.nbr == action_nbr) nbr = counter
    })
    return nbr
}