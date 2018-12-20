import React, { Component } from 'react';

class Counter extends Component {
  state = {
    count: this.props.counter.value
  };

  formatCount () {
    const { count } = this.state;
    return count === 0 ? 'Zero' : count;
  };

  getBadgeClasses () {
    let classes = "badge m-2 badge-";
    classes += this.state.count === 0 ? "warning" : "primary";
    return classes;
  };

  handleIncrement = () => {
    const count = this.state.count + 1;
    this.setState({count: count});
  };

  handleReset = () => {
    this.setState({count: 0});
  };

  render () {
    return (
      <div>
        {this.props.children}
        <span
          style={{fontSize: 15}}
          className={this.getBadgeClasses()}
        >
          {this.formatCount()}
        </span>

        <button
          onClick={this.handleIncrement}
          style={{fontSize: 20}}
          className="btn btn-success btn-sm"
        >
          Increment
        </button>

        <button
          onClick={this.handleReset}
          style={{fontSize: 20}}
          className="btn btn-dark btn-sm"
        >
          Reset
        </button>
        <button
          onClick={() => this.props.onDelete(this.props.counter.id)}
          style={{fontSize: 20}}
          className="btn btn-danger btn-sm"
        >
          Delete
        </button>
      </div>
    );
  }
}

export default Counter
