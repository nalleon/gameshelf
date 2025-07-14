package es.gameshelf.domain.services;

import es.gameshelf.domain.Genre;
import es.gameshelf.domain.interfaces.repository.IGenreRepository;
import es.gameshelf.domain.interfaces.service.IGenreService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class GenreService implements IGenreService {
    /**
     * Properties
     */
    IGenreRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IGenreRepository repository) {
        this.repository = repository;
    }

    @Override
    public Genre add(String name) {
        Genre item = new Genre();
        item.setName(name);
        return repository.save(item);
    }

    @Override
    public List<Genre> findAll() {
        return repository.findAll();
    }

    @Override
    public Genre findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Genre findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Genre update(Integer id, String name) {
        Genre item = new Genre(id);
        item.setName(name);
        return repository.save(item);    }
}
