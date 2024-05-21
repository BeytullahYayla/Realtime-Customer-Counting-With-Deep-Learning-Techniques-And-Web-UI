import React,{useEffect} from 'react'
import { AreaChart, Area, Rectangle, Pie, PieChart, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PieChartActiveShape from '../components/PieChartActiveShape';
import { Data } from '../data/Data';
import RecordTable from '../components/RecordTable';
import SubCards from '../components/SubCards'
import { useDataByDateRange } from '../data/Fetch';

const LastThreeMonthStats = ({storeName, setLoadingByDateRange }) => {

  const { fetchDataByDateRange } = useDataByDateRange();
  const { lastThreeMonthData, lastThreeMonthCustomerData, weeklyTotalCounts, reverseLastThreeMonthData, customerColors } = Data()

  useEffect(() => {
    if (storeName) {
      const fetchDataByDateRangeAsync = async () => {
        try {
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

  const changeData = lastThreeMonthData.map((entry, index) => {
    const previousEntry = index > 0 ? lastThreeMonthData[index - 1] : null;

    return {
      date: entry.DateTime,
      TotalCount: entry.TotalCount,
      change: previousEntry ? entry.TotalCount - previousEntry.TotalCount : 0
    };
  })

  const gradientOffset = () => {
    const dataMax = Math.max(...changeData.map((i) => i.change));
    const dataMin = Math.min(...changeData.map((i) => i.change));
    if (dataMax <= 0) { return 0; }
    if (dataMin >= 0) { return 1; }
    return dataMax / (dataMax - dataMin);
  };
  const off = gradientOffset();

  const monthlyTotalCounts = {};

  lastThreeMonthData.forEach(item => {
    const month = item.DateTime.substring(0, 7);

    if (monthlyTotalCounts[month]) {
      monthlyTotalCounts[month].WomanCount += item.WomanCount;
      monthlyTotalCounts[month].ManCount += item.ManCount;
      monthlyTotalCounts[month].KidCount += item.KidCount;
      monthlyTotalCounts[month].StaffCount += item.StaffCount;
      monthlyTotalCounts[month].EmployeeCount += item.EmployeeCount;
      monthlyTotalCounts[month].TotalCount += item.TotalCount;
    } else {
      monthlyTotalCounts[month] = {
        WomanCount: item.WomanCount,
        ManCount: item.ManCount,
        KidCount: item.KidCount,
        StaffCount: item.StaffCount,
        EmployeeCount: item.EmployeeCount,
        TotalCount: item.TotalCount
      };
    }
  });

  const monthlyTotalCountsArray = Object.entries(monthlyTotalCounts).map(([DateTime, TotalCounts]) => ({
    DateTime,
    ...TotalCounts
  }));

  return (
    <main className='main-container'>
      <div>
        <div className='main-title'>
          <h2>LAST 3 MONTHS STATISTICS</h2>
        </div>
        <div>
          <SubCards data={lastThreeMonthData} />
        </div>
        <div className='charts'>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              width={500}
              height={300}
              data={monthlyTotalCountsArray}
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
              <Tooltip contentStyle={{color:'rgba(64,64,64,0.8)'}} />
              <Legend />
              <Area type="monotone" dataKey="ManCount" stackId="1" stroke="#6A93C3" fill="#87CEEB" activeDot={{ r: 15 }} />
              <Area type="monotone" dataKey="WomanCount" stackId="1" stroke="#C4878E" fill="#FFC0CB" activeDot={{ r: 15 }} />
              <Area type="monotone" dataKey="KidCount" stackId="1" stroke="#ee9a00" fill="#ffb90f" activeDot={{ r: 15 }} />
            </AreaChart>
          </ResponsiveContainer>

          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              width={500}
              height={300}
              data={weeklyTotalCounts}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip contentStyle={{color:'rgba(64,64,64,0.8)'}} />
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
                data={lastThreeMonthCustomerData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomizedLabel}
                outerRadius={125}
                fill="#8884d8"
                dataKey="TotalCustomer"
              >
                {lastThreeMonthCustomerData.map((entry, index) => (
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
              <XAxis dataKey="DateTime" />
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
            <PieChartActiveShape data={monthlyTotalCountsArray} />
          </ResponsiveContainer>
        </div>
        <div className='main-title' style={{ marginTop: 50 }}>
          <h2>LAST 3 MONTHS RECORDS</h2>
        </div>
        <RecordTable data={reverseLastThreeMonthData} />
      </div>
    </main>
  )
}

export default LastThreeMonthStats