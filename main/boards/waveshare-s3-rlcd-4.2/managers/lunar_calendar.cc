#include "lunar_calendar.h"

#include <cstdint>

namespace {

// 1900-2100 年农历编码表（下标 = 年份 - 1900）
//   bit0-3  ：闰月月份（0 表示无闰月）
//   bit4-15 ：1-12 月大小月，1 = 30 天，0 = 29 天
//   bit16   ：闰月天数，1 = 30 天，0 = 29 天
const uint32_t kLunarInfo[201] = {
    // 1900-1909
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    // 1910-1919
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    // 1920-1929
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    // 1930-1939
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    // 1940-1949
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    // 1950-1959
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
    // 1960-1969
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    // 1970-1979
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
    // 1980-1989
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    // 1990-1999
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    // 2000-2009
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    // 2010-2019
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    // 2020-2029
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    // 2030-2039
    0x05aa0, 0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    // 2040-2049
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    // 2050-2059
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
    // 2060-2069
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    // 2070-2079
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    // 2080-2089
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    // 2090-2099
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
    // 2100
    0x0d520,
};

constexpr int kMinYear = 1900;
constexpr int kMaxYear = 2100;

// 该农历年的闰月月份，0 表示无闰月
int LeapMonth(int year) {
    return static_cast<int>(kLunarInfo[year - kMinYear] & 0xF);
}

// 闰月天数，无闰月返回 0
int LeapMonthDays(int year) {
    if (LeapMonth(year) == 0) return 0;
    return (kLunarInfo[year - kMinYear] & 0x10000) ? 30 : 29;
}

// 指定农历月的天数
int MonthDays(int year, int month) {
    if (month < 1 || month > 12) return 29;
    return (kLunarInfo[year - kMinYear] & (0x10000u >> month)) ? 30 : 29;
}

// 该农历年的总天数
int YearDays(int year) {
    int sum = 348;  // 12 * 29
    for (uint32_t bit = 0x8000; bit >= 0x10; bit >>= 1) {
        if (kLunarInfo[year - kMinYear] & bit) sum++;
    }
    return sum + LeapMonthDays(year);
}

// 公历日期 -> 距 1970-01-01 的天数（Howard Hinnant 算法，无时区依赖）
int64_t DaysFromCivil(int y, unsigned m, unsigned d) {
    y -= (m <= 2) ? 1 : 0;
    const int64_t era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const unsigned doy = (153u * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + static_cast<int64_t>(doe) - 719468;
}

}  // namespace

bool SolarToLunar(int year, int month, int day, LunarDate* out) {
    if (out == nullptr) return false;
    if (year < 1900 || year > 2100 || month < 1 || month > 12 || day < 1 || day > 31) {
        return false;
    }

    // 1900-01-31 是农历 1900 年正月初一
    int64_t offset = DaysFromCivil(year, static_cast<unsigned>(month), static_cast<unsigned>(day))
                   - DaysFromCivil(1900, 1, 31);

    // 逐农历年扣减，得到农历年
    int lunarYear = kMinYear;
    while (lunarYear <= kMaxYear) {
        const int yd = YearDays(lunarYear);
        if (offset < yd) break;
        offset -= yd;
        lunarYear++;
    }
    if (lunarYear > kMaxYear) return false;

    // 年份内 1-based 的第几天
    int64_t day_in_year = offset + 1;

    const int leapMonth = LeapMonth(lunarYear);
    int lunarMonth = 1;
    bool isLeap = false;

    for (int m = 1; m <= 12; ++m) {
        const int md = MonthDays(lunarYear, m);
        if (day_in_year <= md) {
            lunarMonth = m;
            isLeap = false;
            break;
        }
        day_in_year -= md;

        // 正常月之后插入闰月（闰月的序号与前一月相同）
        if (leapMonth == m) {
            const int lmd = LeapMonthDays(lunarYear);
            if (day_in_year <= lmd) {
                lunarMonth = m;
                isLeap = true;
                break;
            }
            day_in_year -= lmd;
        }
    }

    out->year = lunarYear;
    out->month = lunarMonth;
    out->day = static_cast<int>(day_in_year);
    out->leap = isLeap;
    return true;
}

std::string LunarToChinese(const LunarDate& d) {
    static const char* kMonthNames[13] = {
        "", "正月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "冬月", "腊月",
    };
    static const char* kDayNames[31] = {
        "",
        "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十",
    };

    if (d.month < 1 || d.month > 12 || d.day < 1 || d.day > 30) {
        return std::string();
    }

    std::string text;
    if (d.leap) text += "闰";
    text += kMonthNames[d.month];
    text += kDayNames[d.day];
    return text;
}
