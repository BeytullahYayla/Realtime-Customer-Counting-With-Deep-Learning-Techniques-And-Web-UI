import { useState } from "react";
import axios from "axios";
import {jwtDecode} from 'jwt-decode';

let data = []
let stores = []
let lastThreeMonthData = []
let lastMonthData = []
let lastWeekData = []
let todayData = []
let users = []

export function setData(newData){
  data = newData;
}

export function setLastThreeMonthData(newLastThreeMonthData){
  lastThreeMonthData = newLastThreeMonthData;
}

export function setLastMonthData(newLastMonthData){
  lastMonthData = newLastMonthData;
}

export function setLastWeekData(newLastWeekData){
  lastWeekData = newLastWeekData;
}

export function setTodayData(newTodayData){
  todayData = newTodayData;
}

export function setStores(newStores){
  stores = newStores
}

export function setUsers(newUsers){
  users = newUsers
}

export function getData(){
  return data;
}

export function getLastThreeMonthData(){
  return lastThreeMonthData;
}

export function getLastMonthData(){
  return lastMonthData;
}

export function getLastWeekData(){
  return lastWeekData;
}

export function getTodayData(){
  return todayData;
}

export function getStores(){
  return stores;
}

export function getUsers(){
  return users;
}

let userRole = localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).role : ""

export function setUserRole(newUserRole){
  userRole = newUserRole;
}

export function getUserRole(){
  return userRole;
}

export const useData = () => {

  const fetchData = async (storeName) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/stores/${storeName}/counts`
      );
      setData(response.data);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return { fetchData };
};

export const useDataByDateRange = () => {

  const fetchDataByDateRange = async (storeName, dateRange) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/stores/${storeName}/counts/${dateRange}`
      );
      if(dateRange === "1 DAY"){
        setTodayData(response.data)
      }else if(dateRange === "1 WEEK"){
        setLastWeekData(response.data)
      }else if(dateRange === "1 MONTH"){
        setLastMonthData(response.data)
      }else if(dateRange === "3 MONTH"){
        setLastThreeMonthData(response.data)
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return { fetchDataByDateRange };
};

export const useStores = () => {

  const fetchStores = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/stores`);
      setStores(response.data);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return { fetchStores };
};

export const useUsers = () => {
  const fetchUsers = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/users`);
      setUsers(response.data);
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return { fetchUsers };
};
