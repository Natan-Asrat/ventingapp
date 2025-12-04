def optimize_notification_queryset(qs):
    return qs.select_related(
        "report_decision",
        "report_decision__report",

        "report_decision__report__reported_post",
        "report_decision__report__reported_post__posted_by",

        "report_decision__report__reported_connection",
        "report_decision__report__reported_transaction",

        "report_decision__report__reported_connection__connected_user",
        "report_decision__report__reported_connection__initiating_user",

        "report_decision__report__reported_message__user", 
        "report_decision__report__reported_message__reply_to", 
        "report_decision__report__reported_message__reply_to__user", 
        "report_decision__report__reported_message__shared_post", 
        "report_decision__report__reported_message__shared_post__posted_by",
        "report_decision__report__reported_message__reply_to__forwarded_from",
        "report_decision__report__reported_message__reply_to__forwarded_from__user",
        "report_decision__report__reported_message__reply_to__shared_post",
        "report_decision__report__reported_message__reply_to__shared_post__posted_by",
        "report_decision__report__reported_message__forwarded_from",
        "report_decision__report__reported_message__forwarded_from__user",
        "report_decision__report__reported_message__forwarded_from__shared_post",
        "report_decision__report__reported_message__forwarded_from__shared_post__posted_by",
    
    ).prefetch_related(
        "report_decision__report__decisions",

        "report_decision__report__reported_post__payment_info_list",

        "report_decision__report__reported_message__shared_post__payment_info_list",
        "report_decision__report__reported_message__reply_to__shared_post__payment_info_list",
        "report_decision__report__reported_message__forwarded_from__shared_post__payment_info_list"
    )