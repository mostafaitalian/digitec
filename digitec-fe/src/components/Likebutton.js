import cx from 'classnames';
import React,{ Component } from 'react';

export default class LikeButton extends Component {
    state={
        counter:100,
        isLiked:false,
    }
    handleDoubleClick= (e)=>{
        if(this.state.isLiked ===true){
            this.setState((prev)=>{
                if (prev.isLiked === false){
                    return{
                        counter: prev.counter +1,
                        isLiked : true
                    }

                }
                else if(prev.isliked ===true) 
                return{
                    counter: prev.counter -1,
                    isLiked : false
                }
            })
        }
    }
    handle_onClick = (e)=>{
        if (this.state.isliked === false){
            this.setState((prev)=>{
                return{
                    counter: prev.counter + 1,
                    isLiked: true,
                }
            })
        }
    }
    render() {
        let liked_classes = cx({
            'like_button': true,
            'liked':this.state.isLiked,

        })
        return (
            <>
                <div>
                    <h2>Like Button</h2>
                    <button className={liked_classes} onDoubleClick={this.handleDoubleClick} onClick={this.handle_onClick}>Like<span> | {this.state.counter}</span></button>



                </div>
                <style>{`
                    .like-button {
                        font-size: 1rem;
                        padding: 5px 10px;
                        color:  #585858;
                    }
                   .liked {
                        font-weight: bold;
                        color: #1565c0;
                   }
                `}</style>
            </>
        );
    }
}