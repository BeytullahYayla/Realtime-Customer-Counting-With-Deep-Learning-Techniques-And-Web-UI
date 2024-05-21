import React from 'react'
import FaceIcon from '@mui/icons-material/Face';
import Face3Icon from '@mui/icons-material/Face3';
import ChildCareIcon from '@mui/icons-material/ChildCare';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';

const SubCards = ({data}) => {
        
      if (!data) {
        return <div>Loading...</div>; // veya başka bir yükleme göstergesi
      }

    return (
        <div className='main-cards'>
            <div className='subcard'>
                <div className='card-inner'>
                    <h3>TOTAL MAN</h3>
                    <FaceIcon className='subcard_icon' />
                </div>
                <h1>{data.reduce((sum, day) => sum + day.ManCount, 0)}</h1>
            </div>
            <div className='subcard'>
                <div className='card-inner'>
                    <h3>TOTAL WOMAN</h3>
                    <Face3Icon className='subcard_icon' />
                </div>
                <h1>{data.reduce((sum, day) => sum + day.WomanCount, 0)}</h1>
            </div>
            <div className='subcard'>
                <div className='card-inner'>
                    <h3>TOTAL KID</h3>
                    <ChildCareIcon className='subcard_icon' />
                </div>
                <h1>{data.reduce((sum, day) => sum + day.KidCount, 0)}</h1>
            </div>
            <div className='subcard'>
                <div className='card-inner'>
                    <h3>TOTAL STAFF & EMPLOYEE</h3>
                    <SupportAgentIcon className='subcard_icon' />
                </div>
                <h1>{data.reduce((sum, day) => sum + day.StaffCount, 0)} | {data.reduce((sum, day) => sum + day.EmployeeCount, 0)}</h1>
            </div>
        </div>
    )
}

export default SubCards