import React from 'react'
import { BsCalendarMonthFill, BsCalendarFill, BsCalendarWeekFill, BsCalendarDateFill } from 'react-icons/bs'
import {Data} from '../data/Data';


const MainCards = () => {

    const {lastWeekData, lastMonthData, lastThreeMonthData, todayData} = Data()
    
    
      if (!lastThreeMonthData) {
        return <div>Loading...</div>; // veya başka bir yükleme göstergesi
      }

    return (
        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>LAST 3 MONTHS</h3>
                    <BsCalendarFill className='card_icon' />
                </div>
                <h1>{lastThreeMonthData.reduce((sum, day) => sum + day.TotalCount, 0)}</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>LAST MONTH</h3>
                    <BsCalendarMonthFill className='card_icon' />
                </div>
                <h1>{lastMonthData.reduce((sum, day) => sum + day.TotalCount, 0)}</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>LAST WEEK</h3>
                    <BsCalendarWeekFill className='card_icon' />
                </div>
                <h1>{lastWeekData.reduce((sum, day) => sum + day.TotalCount, 0)}</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>TODAY</h3>
                    <BsCalendarDateFill className='card_icon' />
                </div>
                <h1>{todayData.reduce((sum, day) => sum + day.TotalCount, 0)}</h1>
            </div>
        </div>
    )
}

export default MainCards