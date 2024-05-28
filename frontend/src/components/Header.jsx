import React, { useState } from 'react'
import { BsPersonCircle, BsJustify } from 'react-icons/bs'
import Selection from './Selection'
import { Link } from 'react-router-dom';

function Header({ OpenSidebar, setLoading, setLoadingByDateRange, setStoreName }) {
  const [isTooltipVisible, setIsTooltipVisible] = useState(true);
  const username = localStorage.getItem('username');

  const toggleTooltip = () => {
    setIsTooltipVisible(!isTooltipVisible);
  };

  return (
    <header className='header'>
      <div className='menu-icon'>
        <BsJustify className='icon' onClick={OpenSidebar} />
      </div>
      <div className='header-left'/>
      <div className='header-center'>
        <Selection setLoading={setLoading} setLoadingByDateRange={setLoadingByDateRange} setStoreName={setStoreName} />
      </div>
      <div className='header-right'>
        <Link to="/Account">
          <BsPersonCircle className='icon person-icon' onMouseEnter={toggleTooltip} />
        </Link>
        {isTooltipVisible && username ? (
          <div className='tooltip'>
            {username}
          </div>
        ) : ("")}
      </div>
    </header>
  )
}

export default Header