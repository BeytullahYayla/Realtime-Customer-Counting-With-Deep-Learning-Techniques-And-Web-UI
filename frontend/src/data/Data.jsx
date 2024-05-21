import { getData, getLastThreeMonthData, getLastMonthData, getLastWeekData, getTodayData } from "./Fetch";

export const Data = () => {
  const data = getData();
  const lastThreeMonthData = getLastThreeMonthData();
  const lastMonthData = getLastMonthData();
  const lastWeekData = getLastWeekData();
  const todayData = getTodayData();

  const calculateCustomerTypeData = (data) => {
    const TotalWomanCount = data.reduce(
      (acc, entry) => acc + entry.WomanCount, 0
    );
    const TotalManCount = data.reduce(
      (acc, entry) => acc + entry.ManCount, 0
    );
    const TotalKidCount = data.reduce(
      (acc, entry) => acc + entry.KidCount, 0
    );
    return [
      { CustomerType: "Woman", TotalCustomer: TotalWomanCount },
      { CustomerType: "Man", TotalCustomer: TotalManCount },
      { CustomerType: "Kid", TotalCustomer: TotalKidCount },
    ];
  };

  const lastWeekCustomerData = calculateCustomerTypeData(lastWeekData);
  const lastMonthCustomerData = calculateCustomerTypeData(lastMonthData);
  const lastThreeMonthCustomerData = calculateCustomerTypeData(lastThreeMonthData);

  const daysOfWeek = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  const getTotalCountByDayOfWeek = (data, dayOfWeek) => {
    let WomanCount = 0;
    let ManCount = 0;
    let KidCount = 0;
    let StaffCount = 0;
    let EmployeeCount = 0;
    let TotalCustomers = 0;
    let TotalWorkers = 0;
    let TotalCount = 0;

    data.forEach((entry) => {
      const date = new Date(entry.DateTime);
      const entryDayOfWeek = date.getDay();
      if (entryDayOfWeek === dayOfWeek) {
        WomanCount += entry.WomanCount;
        ManCount += entry.ManCount;
        KidCount += entry.KidCount;
        StaffCount += entry.StaffCount;
        EmployeeCount += entry.EmployeeCount;
        TotalCustomers += entry.TotalCustomers;
        TotalWorkers += entry.TotalWorkers;
        TotalCount += entry.TotalCount;
      }
    });

    return { WomanCount, ManCount, KidCount, StaffCount, EmployeeCount, TotalCustomers, TotalWorkers, TotalCount };
  };

  const weeklyTotalCounts = daysOfWeek.map((day, index) => {
    const { WomanCount, ManCount, KidCount, StaffCount, EmployeeCount, TotalCustomers, TotalWorkers, TotalCount } = getTotalCountByDayOfWeek(
      lastThreeMonthData,
      index
    );
    return { day, WomanCount, ManCount, KidCount, StaffCount, EmployeeCount, TotalCustomers, TotalWorkers, TotalCount };
  });

  const reverseData = [...data].reverse();
  const reverseLastThreeMonthData = [...lastThreeMonthData].reverse();
  const reverseLastMonthData = [...lastMonthData].reverse();
  const reverseLastWeekData = [...lastWeekData].reverse();

  const customerColors = ["#C4878E", "#6A93C3", "#ffb90f"];

  return {
    data,
    lastThreeMonthData,
    lastMonthData,
    lastWeekData,
    todayData,
    lastWeekCustomerData,
    lastMonthCustomerData,
    lastThreeMonthCustomerData,
    weeklyTotalCounts,
    reverseData,
    reverseLastThreeMonthData,
    reverseLastMonthData,
    reverseLastWeekData,
    customerColors
  };
};
