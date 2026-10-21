#ifndef __LUNAR_CALENDAR_H__
#define __LUNAR_CALENDAR_H__

#include <string>

// 农历日期（离线换算，无需网络）
struct LunarDate {
    int year = 0;       // 农历年，如 2026
    int month = 0;      // 1-12
    int day = 0;        // 1-30
    bool leap = false;  // 是否为闰月
};

// 公历 -> 农历，支持 1900-01-31 ~ 2100-12-31，超出范围返回 false
bool SolarToLunar(int year, int month, int day, LunarDate* out);

// 农历 -> 中文，如 "八月廿一"、"闰六月初一"
std::string LunarToChinese(const LunarDate& d);

#endif
