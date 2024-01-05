//
//  DateExtension.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/18/23.
//

import Foundation

extension Date {
    init(milliseconds: Int64) {
        self = Date(timeIntervalSince1970: TimeInterval(milliseconds) / 1000)
    }
}
