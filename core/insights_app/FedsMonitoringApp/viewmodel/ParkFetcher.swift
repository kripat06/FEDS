//
//  ParkFetcher.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/9/23.
//

import Foundation

class ParkFetcher: ObservableObject {
    @Published var parks:[Park] = [Park]()

    private let service = APIService()

    func fetchParks() {
        service.fetchAllParks() { result in
            DispatchQueue.main.async {
                switch result {
                    case .success(let parks):
                        self.parks = parks
                        print(self.parks)
                    case .failure(let error):
                        print("Could not load: \(error)")
                }
            }
        }
    }
}
