import * as React from 'react';
import {Data} from '../data/Data'
import RecordTable from '../components/RecordTable';

function Records() {
    const {reverseData} = Data()
    return (
        <main className='main-container'>
            <div>
                <div className='main-title'>
                    <h2>RECORDS</h2>
                </div>
                <RecordTable data={reverseData} />
            </div>
        </main>
    );
}

export default Records