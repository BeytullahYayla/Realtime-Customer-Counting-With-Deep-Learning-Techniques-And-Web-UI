import React, { useEffect } from 'react'
import { AreaChart, Area, Rectangle, Pie, PieChart, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PieChartActiveShape from '../components/PieChartActiveShape';
import { Data } from '../data/Data';
import MainCards from '../components/MainCards';
import RecordTable from '../components/RecordTable';
import { useDataByDateRange } from '../data/Fetch';
import SubCards from '../components/SubCards';


function Home({ storeName, setLoadingByDateRange }) {

    const { fetchDataByDateRange } = useDataByDateRange();
    const { lastWeekData, lastWeekCustomerData, reverseLastWeekData, customerColors } = Data()

    useEffect(() => {
        if (storeName) {
            const fetchDataByDateRangeAsync = async () => {
                try {
                    await fetchDataByDateRange(storeName, "1 DAY");
                    await fetchDataByDateRange(storeName, "1 WEEK");
                    await fetchDataByDateRange(storeName, "1 MONTH");
                    await fetchDataByDateRange(storeName, "3 MONTH");
                    setLoadingByDateRange(false);
                } catch (error) {
                    console.error("Veri çekme hatası:", error);
                    setLoadingByDateRange(false);
                }
            };

            fetchDataByDateRangeAsync();
        }
    }, [fetchDataByDateRange, storeName]);

    const RADIAN = Math.PI / 180;
    const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    const changeData = lastWeekData.map((entry, index) => {
        const previousEntry = index > 0 ? lastWeekData[index - 1] : null;

        return {
            date: entry.date,
            TotalCount: entry.TotalCount,
            change: previousEntry ? entry.TotalCount - previousEntry.TotalCount : 0
        };
    })

    const gradientOffset = () => {
        const dataMax = Math.max(...changeData.map((i) => i.change));
        const dataMin = Math.min(...changeData.map((i) => i.change));

        if (dataMax <= 0) {
            return 0;
        }
        if (dataMin >= 0) {
            return 1;
        }

        return dataMax / (dataMax - dataMin);
    };

    const off = gradientOffset();


    return (
        <main className='main-container'>
            <div>
                <div className='main-title'>
                    <h2>DASHBOARD</h2>
                </div>
                <MainCards />
                <div className='main-title'>
                    <h2>LAST WEEK STATISTICS</h2>
                </div>
                <div className='charts'>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                            width={500}
                            height={300}
                            data={lastWeekData}
                            margin={{
                                top: 5,
                                right: 30,
                                left: 20,
                                bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="DateTime" />
                            <YAxis />
                            <Tooltip contentStyle={{backgroundColor:'rgba(64,64,64,0.8)'}} />
                            <Legend />
                            <Bar dataKey="ManCount" fill="#87CEEB" activeBar={<Rectangle fill="#6A93C3" stroke="#FFD700" />} />
                            <Bar dataKey="WomanCount" fill="#FFC0CB" activeBar={<Rectangle fill="#C4878E" stroke="#FFD700" />} />
                            <Bar dataKey="KidCount" fill="#ffb90f" activeBar={<Rectangle fill="#ee9a00" stroke="#FFD700" />} />
                        </BarChart>
                    </ResponsiveContainer>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                            width={500}
                            height={300}
                            data={lastWeekData}
                            margin={{
                                top: 5,
                                right: 30,
                                left: 20,
                                bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="DateTime" />
                            <YAxis />
                            <Tooltip contentStyle={{backgroundColor:'rgba(64,64,64,0.8)'}} />
                            <Legend />
                            <Bar dataKey="TotalCustomers" stackId="1" fill="#80C986" activeBar={<Rectangle fill="#689775" stroke="#FFD700" />} />
                            <Bar dataKey="TotalWorkers" stackId="1" fill="#ab82ff" activeBar={<Rectangle fill="#5d478b" stroke="#FFD700" />} />
                        </BarChart>
                    </ResponsiveContainer>

                </div>
                <div className='charts-three'>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart width={400} height={400}>
                            <Pie
                                data={lastWeekCustomerData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={renderCustomizedLabel}
                                outerRadius={125}
                                fill="#8884d8"
                                dataKey="TotalCustomer"
                            >
                                {lastWeekCustomerData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={customerColors[index % customerColors.length]} />
                                ))}
                            </Pie>
                        </PieChart>
                    </ResponsiveContainer>
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart
                            width={500}
                            height={400}
                            data={changeData}
                            margin={{
                                top: 10,
                                right: 30,
                                left: 0,
                                bottom: 0,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis />
                            <Tooltip />
                            <defs>
                                <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset={off} stopColor="lime" stopOpacity={1} />
                                    <stop offset={off} stopColor="#ff3030" stopOpacity={1} />
                                </linearGradient>
                            </defs>
                            <Area type="monotone" dataKey="change" stroke="#000" fill="url(#splitColor)" />
                        </AreaChart>
                    </ResponsiveContainer>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChartActiveShape data={lastWeekData} />
                    </ResponsiveContainer>

                </div>
                <div className='main-title' style={{ marginTop: 50 }}>
                    <h2>LAST WEEK RECORDS</h2>
                </div>
                <RecordTable data={reverseLastWeekData} />
            </div>
        </main>
    )
}

export default Home
