import streamlit as st

# --- 1. Konfiguracja i Stan Aplikacji (Streamlit Session State) ---

# Tytuł aplikacji
st.title("🛒 Prosta Aplikacja Magazynowa")
st.caption("Aplikacja do zarządzania nazwami produktów bez ilości i cen.")

# Inicjalizacja "magazynu" w Session State. 
# Session State gwarantuje, że lista produktów jest zachowana pomiędzy interakcjami.
if 'inventory' not in st.session_state:
    st.session_state.inventory = ["Młotek", "Śrubokręt", "Wkręty M4"] # Przykładowe produkty

# --- 2. Funkcje Logiczne (Dodawanie i Usuwanie) ---

def add_product():
    """ 
    Pobiera nazwę produktu z pola tekstowego i dodaje ją do Session State.
    """
    product_name = st.session_state.product_input
    
    if product_name:
        # Dodanie do listy w Session State
        st.session_state.inventory.append(product_name)
        st.success(f"Dodano: **{product_name}**")
        # Wyczyść pole tekstowe po dodaniu
        st.session_state.product_input = "" 
    else:
        st.warning("Nazwa produktu nie może być pusta.")

def remove_product(product_to_remove):
    """ 
    Usuwa określony produkt z Session State.
    """
    try:
        st.session_state.inventory.remove(product_to_remove)
        st.info(f"Usunięto: **{product_to_remove}**")
        # st.rerun() jest kluczowe w tym przypadku, aby odświeżyć listę
        st.rerun() 
    except ValueError:
        # To się nie powinno zdarzyć, jeśli przycisk działa poprawnie, ale jest to zabezpieczenie.
        st.error(f"Błąd: Produkt '{product_to_remove}' nie znaleziono.")


# --- 3. Interfejs Użytkownika (UI) Streamlit ---

st.header("➕ Dodaj Nowy Produkt")

# Użycie formularza (st.form) do grupowania elementów
with st.form("add_form", clear_on_submit=True):
    # Pole tekstowe dla nazwy produktu. Używamy 'key', aby odwołać się do jego wartości w funkcji.
    st.text_input("Nazwa produktu:", key="product_input")
    
    # Przycisk, który wywoła funkcję 'add_product'
    submitted = st.form_submit_button("Dodaj do Magazynu", on_click=add_product)


st.markdown("---")

st.header("📦 Aktualny Magazyn")

if not st.session_state.inventory:
    st.info("Magazyn jest obecnie pusty. Dodaj pierwszy produkt powyżej!")
else:
    # Wyświetlanie jako tabela (DataFrame), co Streamlit robi ładnie domyślnie.
    # Wymaga importu pandas, ale dla prostoty użyjemy listy z przyciskiem.
    
    # Możemy wyświetlić produkty jako listę, umożliwiając usunięcie każdego z osobna
    for product in st.session_state.inventory:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"**{product}**")
            
        with col2:
            # Tworzymy unikalny klucz dla każdego przycisku "Usuń"
            if col2.button("Usuń", key=f"del_{product}"):
                remove_product(product)
