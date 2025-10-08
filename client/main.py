from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()


def menu():
    while True:
        print("\nWatchlist Manager - Main Menu")
        print("---- USER MANAGEMENT ----")
        print("1. Add User")
        print("2. List Users")
        print("3. Get User by ID")
        print("4. Update User")
        print("5. Delete User")
        print("\n---- TITLE MANAGEMENT ----")
        print("6. Add Title (Movie/Show/Anime)")
        print("7. List All Titles")
        print("8. Search Titles")
        print("9. Update Title")
        print("10. Delete Title")
        print("\n---- WATCHLIST MANAGEMENT ----")
        print("11. Add to Watchlist")
        print("12. Get User Watchlist")
        print("13. Get User Watchlist by Status")
        print("14. Update Watchlist Entry")
        print("15. Remove from Watchlist")
        print("\n0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            print(user_service.create_user(name, email))

        elif choice == "2":
            print(user_service.list_users())

        elif choice == "3":
            user_id = input("Enter User ID: ")
            print(user_service.get_user(user_id))

        elif choice == "4":
            user_id = input("Enter User ID: ")
            name = input("Enter new name (leave blank to skip): ") or None
            email = input("Enter new email (leave blank to skip): ") or None
            print(user_service.update_user(user_id, name, email))

        elif choice == "5":
            user_id = input("Enter User ID: ")
            print(user_service.delete_user(user_id))

        elif choice == "6":
            title = input("Enter title name: ")
            t_type = input("Enter type (movie/show/anime): ")
            genre = input("Enter genre (optional): ") or None
            print(title_service.add_title(title, t_type, genre))

        elif choice == "7":
            print(title_service.list_all_titles())

        elif choice == "8":
            query = input("Enter title/genre keyword: ")
            print(title_service.search_titles(query))

        elif choice == "9":
            movie_id = input("Enter Movie/Show ID: ")
            title = input("Enter new title (leave blank to skip): ") or None
            t_type = input("Enter new type (movie/show/anime, leave blank to skip): ") or None
            print(title_service.update_title(movie_id, title, t_type))

        elif choice == "10":
            movie_id = input("Enter Movie/Show ID: ")
            print(title_service.delete_title(movie_id))

        elif choice == "11":
            user_id = input("Enter User ID: ")
            movie_id = input("Enter Movie/Show ID: ")
            status = input("Enter status (watched/planning/dropped): ")
            rating = input("Enter rating (1-10, optional): ") or None
            review = input("Enter review (optional): ") or None
            print(watchlist_service.add_to_watchlist(user_id, movie_id, status, rating, review))

        elif choice == "12":
            user_id = input("Enter User ID: ")
            print(watchlist_service.get_user_watchlist(user_id))

        elif choice == "13":
            user_id = input("Enter User ID: ")
            status = input("Enter status filter (watched/planning/dropped): ")
            print(watchlist_service.get_user_watchlist_by_status(user_id, status))

        elif choice == "14":
            watchlist_id = input("Enter Watchlist ID: ")
            status = input("Enter new status (leave blank to skip): ") or None
            rating = input("Enter new rating (leave blank to skip): ") or None
            review = input("Enter new review (leave blank to skip): ") or None
            print(watchlist_service.update_watchlist_entry(watchlist_id, status, rating, review))

        elif choice == "15":
            watchlist_id = input("Enter Watchlist ID: ")
            print(watchlist_service.remove_from_watchlist(watchlist_id))

        elif choice == "0":
            print("👋 Exiting Watchlist Manager. Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    menu()
