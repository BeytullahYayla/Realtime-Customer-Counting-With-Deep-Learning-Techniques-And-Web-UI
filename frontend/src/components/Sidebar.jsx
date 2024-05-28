import React from 'react'
import { Link } from 'react-router-dom';
import { BsFillPersonLinesFill, BsJournalBookmarkFill, BsGrid1X2Fill, BsCalendarMonthFill, BsPersonFillLock, BsCalendarFill, BsBoxArrowRight } from 'react-icons/bs'
import { getUserRole } from '../data/Fetch';
import LogoutIcon from '@mui/icons-material/Logout';

function Sidebar({ openSidebarToggle, OpenSidebar }) {
    const role = getUserRole()

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        window.location.reload();
    };

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
                {
                    role === "superuser" ?
                        (<li className='sidebar-list-item'>
                            <Link to="/UserManagement">
                                <BsFillPersonLinesFill className='icon' /> User Management
                            </Link>
                        </li>)
                        : ""
                }
                <li className='sidebar-list-item logout-item' onClick={handleLogout} style={{ marginTop: 'auto' }}>
                    <LogoutIcon className='icon' /> Logout
                </li>

            </ul>
        </aside>
    )
}

export default Sidebar