window.addEventListener('load', (event) => {

    let date_now = new Date();
    let post_start_date = new Date(1631808480000);
    let post_end_date = new Date(1631820360000);

    console.log(post_start_date);
    console.log(post_end_date);

    let date_and_times = getDateAndTimes(post_start_date, post_end_date, date_now);

    console.log(date_and_times);

    if(shouldShow(date_and_times)) {
        console.log('mostrar');
    }
    

});

function getDateAndTimes(post_start_date, post_end_date, date_now)
{

    let object_with_dates;
    
    object_with_dates = {
        now: {
            date_sum: getSumDate(date_now),
            hour: date_now.getHours(),
            minute: date_now.getMinutes(),
            second: date_now.getSeconds()
        },
        start: {
            date_sum: getSumDate(post_start_date),
            hour: post_start_date.getHours(),
            minute: post_start_date.getMinutes(),
            second: post_start_date.getSeconds()
        },
        end: {
            date_sum: getSumDate(post_end_date),
            hour: post_start_date.getHours(),
            minute: post_end_date.getMinutes(),
            second: post_end_date.getSeconds()
        },
    };


    return object_with_dates;
}

function shouldShow(date_and_times)
{
    if(betweenStartEnd(date_and_times.now.date_sum, date_and_times.start.date_sum, date_and_times.end.date_sum)) {
        if(betweenStartEnd(date_and_times.now.hour, date_and_times.start.hour, date_and_times.end.hour)) {
            if(betweenStartEnd(date_and_times.now.second, date_and_times.start.second, date_and_times.end.second)) {
                return true;
            }
        }
    }

    return false;
}

function getSumDate(date_object)
{
    return date_object.getFullYear() + date_object.getMonth() + date_object.getDay();
}

function betweenStartEnd(now_value, start_value, end_value)
{
    return start_value <= now_value && end_value >= now_value;
}
