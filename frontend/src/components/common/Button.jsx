import React from 'react';
export default function Button({ children, onClick, className='' }){
  return <button className={`btn ${className}`} onClick={onClick}>{children}</button>;
}
