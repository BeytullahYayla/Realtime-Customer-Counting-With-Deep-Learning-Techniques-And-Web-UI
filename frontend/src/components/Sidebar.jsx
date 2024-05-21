import React from 'react'
import { Link } from 'react-router-dom';
import { BsJournalBookmarkFill, BsGrid1X2Fill, BsCalendarMonthFill, BsFillGearFill, BsPersonFillLock, BsCalendarFill } from 'react-icons/bs'

function Sidebar({ openSidebarToggle, OpenSidebar }) {
    return (
        <aside id="sidebar" className={openSidebarToggle ? "sidebar-responsive" : ""}>
            <div className='sidebar-title'>
                <div className='sidebar-brand'>
                    <BsPersonFillLock className='icon_header' /> ADMIN PANEL
                </div>
                <span className='icon close_icon' onClick={OpenSidebar}>X</span>
            </div>

            <ul className='sidebar-list'>
                <li className='sidebar-list-item'>
                    <Link to="/">
                        <BsGrid1X2Fill className='icon' /> Dashboard
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to="/LastMonthStats">
                        <BsCalendarMonthFill className='icon' /> Last Month
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to="/LastThreeMonthStats">
                        <BsCalendarFill className='icon' /> Last 3 Months
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to="/Records">
                        <BsJournalBookmarkFill className='icon' /> Records
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to="/Settings">
                        <BsFillGearFill className='icon' /> Setting
                    </Link>
                </li>
            </ul>
        </aside>
    )
}

export default Sidebar