import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import { getStores, setStores } from '../data/Fetch';



export default function Selection({setLoading,setLoadingByDateRange,setStoreName}) {
    const stores = getStores()
    const options = stores.map(store => ({
        value: store.Name,
        label: store.Name
    }))
    const [selectedOption, setSelectedOption] = useState(options[0]);

    const customStyles = {
        control: (provided) => ({
            ...provided,
            width: 250,
        }),
    };

    useEffect(()=>{
        setStoreName(selectedOption.label)
        setLoading(true)
        setLoadingByDateRange(true)
    },[selectedOption])


    return (
        <div>
            <Select
                defaultValue={selectedOption}
                onChange={setSelectedOption}
                options={options}
                styles={customStyles}
            />
        </div>
    );
}